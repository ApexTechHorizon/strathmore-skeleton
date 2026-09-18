import { HttpException, Injectable, Logger } from '@nestjs/common';
import { CareerPathRequestDto, CareerPathResponseDto } from './dto/career-path.dto';

/**
 * U-CS 1 — adapter for the service built by the assigned team.
 *
 * We do not implement the logic. We call their hosted URL and pass the answer on.
 * Free hosting sleeps, so the first call after a quiet period can be slow — hence
 * the generous timeout.
 */
@Injectable()
export class CareerPathService {
  private readonly log = new Logger(CareerPathService.name);
  private readonly baseUrl = process.env.CAREER_PATH_SERVICE_URL ?? '';
  private readonly timeoutMs = Number(process.env.STUDENT_SERVICE_TIMEOUT_MS ?? 30000);

  async call(body: CareerPathRequestDto): Promise<CareerPathResponseDto> {
    if (!this.baseUrl) {
      throw new HttpException('career-path: CAREER_PATH_SERVICE_URL is not set — no service URL yet', 503);
    }

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const res = await fetch(`${this.baseUrl}/paths`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      if (!res.ok) {
        throw new HttpException(`career-path: upstream returned ${res.status}`, 502);
      }
      return (await res.json()) as CareerPathResponseDto;
    } catch (err) {
      this.log.error(`career-path upstream failed: ${err}`);
      throw new HttpException('career-path: upstream unavailable', 502);
    } finally {
      clearTimeout(timer);
    }
  }

  async status() {
    if (!this.baseUrl) return { module: 'career-path', configured: false };
    try {
      const res = await fetch(`${this.baseUrl}/health`);
      return { module: 'career-path', configured: true, up: res.ok, url: this.baseUrl };
    } catch {
      return { module: 'career-path', configured: true, up: false, url: this.baseUrl };
    }
  }
}
