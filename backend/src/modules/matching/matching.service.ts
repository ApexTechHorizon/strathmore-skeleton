import { HttpException, Injectable, Logger } from '@nestjs/common';
import { MatchingRequestDto, MatchingResponseDto } from './dto/matching.dto';

/**
 * U-CS 2 — adapter for the service built by the assigned team.
 *
 * We do not implement the logic. We call their hosted URL and pass the answer on.
 * Free hosting sleeps, so the first call after a quiet period can be slow — hence
 * the generous timeout.
 */
@Injectable()
export class MatchingService {
  private readonly log = new Logger(MatchingService.name);
  private readonly baseUrl = process.env.MATCHING_SERVICE_URL ?? '';
  private readonly timeoutMs = Number(process.env.STUDENT_SERVICE_TIMEOUT_MS ?? 30000);

  async call(body: MatchingRequestDto): Promise<MatchingResponseDto> {
    if (!this.baseUrl) {
      throw new HttpException('matching: MATCHING_SERVICE_URL is not set — no service URL yet', 503);
    }

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const res = await fetch(`${this.baseUrl}/match`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      if (!res.ok) {
        throw new HttpException(`matching: upstream returned ${res.status}`, 502);
      }
      return (await res.json()) as MatchingResponseDto;
    } catch (err) {
      this.log.error(`matching upstream failed: ${err}`);
      throw new HttpException('matching: upstream unavailable', 502);
    } finally {
      clearTimeout(timer);
    }
  }

  async status() {
    if (!this.baseUrl) return { module: 'matching', configured: false };
    try {
      const res = await fetch(`${this.baseUrl}/health`);
      return { module: 'matching', configured: true, up: res.ok, url: this.baseUrl };
    } catch {
      return { module: 'matching', configured: true, up: false, url: this.baseUrl };
    }
  }
}
