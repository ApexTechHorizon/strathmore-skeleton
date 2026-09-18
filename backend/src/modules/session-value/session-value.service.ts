import { HttpException, Injectable, Logger } from '@nestjs/common';
import { SessionValueRequestDto, SessionValueResponseDto } from './dto/session-value.dto';

/**
 * U-CS 5 — adapter for the service built by the assigned team.
 *
 * We do not implement the logic. We call their hosted URL and pass the answer on.
 * Free hosting sleeps, so the first call after a quiet period can be slow — hence
 * the generous timeout.
 */
@Injectable()
export class SessionValueService {
  private readonly log = new Logger(SessionValueService.name);
  private readonly baseUrl = process.env.SESSION_VALUE_SERVICE_URL ?? '';
  private readonly timeoutMs = Number(process.env.STUDENT_SERVICE_TIMEOUT_MS ?? 30000);

  async call(body: SessionValueRequestDto): Promise<SessionValueResponseDto> {
    if (!this.baseUrl) {
      throw new HttpException('session-value: SESSION_VALUE_SERVICE_URL is not set — no service URL yet', 503);
    }

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const res = await fetch(`${this.baseUrl}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      if (!res.ok) {
        throw new HttpException(`session-value: upstream returned ${res.status}`, 502);
      }
      return (await res.json()) as SessionValueResponseDto;
    } catch (err) {
      this.log.error(`session-value upstream failed: ${err}`);
      throw new HttpException('session-value: upstream unavailable', 502);
    } finally {
      clearTimeout(timer);
    }
  }

  async status() {
    if (!this.baseUrl) return { module: 'session-value', configured: false };
    try {
      const res = await fetch(`${this.baseUrl}/health`);
      return { module: 'session-value', configured: true, up: res.ok, url: this.baseUrl };
    } catch {
      return { module: 'session-value', configured: true, up: false, url: this.baseUrl };
    }
  }
}
