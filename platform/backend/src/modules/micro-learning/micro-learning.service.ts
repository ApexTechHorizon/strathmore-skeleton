import { HttpException, Injectable, Logger } from '@nestjs/common';
import { MicroLearningRequestDto, MicroLearningResponseDto } from './dto/micro-learning.dto';

/**
 * U-CS 8 — adapter for the service built by the assigned team.
 *
 * We do not implement the logic. We call their hosted URL and pass the answer on.
 * Free hosting sleeps, so the first call after a quiet period can be slow — hence
 * the generous timeout.
 */
@Injectable()
export class MicroLearningService {
  private readonly log = new Logger(MicroLearningService.name);
  private readonly baseUrl = process.env.MICRO_LEARNING_SERVICE_URL ?? '';
  private readonly timeoutMs = Number(process.env.STUDENT_SERVICE_TIMEOUT_MS ?? 30000);

  async call(body: MicroLearningRequestDto): Promise<MicroLearningResponseDto> {
    if (!this.baseUrl) {
      throw new HttpException('micro-learning: MICRO_LEARNING_SERVICE_URL is not set — no service URL yet', 503);
    }

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const res = await fetch(`${this.baseUrl}/next`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      if (!res.ok) {
        throw new HttpException(`micro-learning: upstream returned ${res.status}`, 502);
      }
      return (await res.json()) as MicroLearningResponseDto;
    } catch (err) {
      this.log.error(`micro-learning upstream failed: ${err}`);
      throw new HttpException('micro-learning: upstream unavailable', 502);
    } finally {
      clearTimeout(timer);
    }
  }

  async status() {
    if (!this.baseUrl) return { module: 'micro-learning', configured: false };
    try {
      const res = await fetch(`${this.baseUrl}/health`);
      return { module: 'micro-learning', configured: true, up: res.ok, url: this.baseUrl };
    } catch {
      return { module: 'micro-learning', configured: true, up: false, url: this.baseUrl };
    }
  }
}
