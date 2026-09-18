import { HttpException, Injectable, Logger } from '@nestjs/common';
import { AnalyticsRequestDto, AnalyticsResponseDto } from './dto/analytics.dto';

/**
 * U-CS 7 — adapter for the service built by the assigned team.
 *
 * We do not implement the logic. We call their hosted URL and pass the answer on.
 * Free hosting sleeps, so the first call after a quiet period can be slow — hence
 * the generous timeout.
 */
@Injectable()
export class AnalyticsService {
  private readonly log = new Logger(AnalyticsService.name);
  private readonly baseUrl = process.env.ANALYTICS_SERVICE_URL ?? '';
  private readonly timeoutMs = Number(process.env.STUDENT_SERVICE_TIMEOUT_MS ?? 30000);

  async call(body: AnalyticsRequestDto): Promise<AnalyticsResponseDto> {
    if (!this.baseUrl) {
      throw new HttpException('analytics: ANALYTICS_SERVICE_URL is not set — no service URL yet', 503);
    }

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const res = await fetch(`${this.baseUrl}/cohort`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      if (!res.ok) {
        throw new HttpException(`analytics: upstream returned ${res.status}`, 502);
      }
      return (await res.json()) as AnalyticsResponseDto;
    } catch (err) {
      this.log.error(`analytics upstream failed: ${err}`);
      throw new HttpException('analytics: upstream unavailable', 502);
    } finally {
      clearTimeout(timer);
    }
  }

  async status() {
    if (!this.baseUrl) return { module: 'analytics', configured: false };
    try {
      const res = await fetch(`${this.baseUrl}/health`);
      return { module: 'analytics', configured: true, up: res.ok, url: this.baseUrl };
    } catch {
      return { module: 'analytics', configured: true, up: false, url: this.baseUrl };
    }
  }
}
