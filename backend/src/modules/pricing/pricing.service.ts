import { HttpException, Injectable, Logger } from '@nestjs/common';
import { PricingRequestDto, PricingResponseDto } from './dto/pricing.dto';

/**
 * U-CS 6 — adapter for the service built by the assigned team.
 *
 * We do not implement the logic. We call their hosted URL and pass the answer on.
 * Free hosting sleeps, so the first call after a quiet period can be slow — hence
 * the generous timeout.
 */
@Injectable()
export class PricingService {
  private readonly log = new Logger(PricingService.name);
  private readonly baseUrl = process.env.PRICING_SERVICE_URL ?? '';
  private readonly timeoutMs = Number(process.env.STUDENT_SERVICE_TIMEOUT_MS ?? 30000);

  async call(body: PricingRequestDto): Promise<PricingResponseDto> {
    if (!this.baseUrl) {
      throw new HttpException('pricing: PRICING_SERVICE_URL is not set — no service URL yet', 503);
    }

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const res = await fetch(`${this.baseUrl}/price`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      if (!res.ok) {
        throw new HttpException(`pricing: upstream returned ${res.status}`, 502);
      }
      return (await res.json()) as PricingResponseDto;
    } catch (err) {
      this.log.error(`pricing upstream failed: ${err}`);
      throw new HttpException('pricing: upstream unavailable', 502);
    } finally {
      clearTimeout(timer);
    }
  }

  async status() {
    if (!this.baseUrl) return { module: 'pricing', configured: false };
    try {
      const res = await fetch(`${this.baseUrl}/health`);
      return { module: 'pricing', configured: true, up: res.ok, url: this.baseUrl };
    } catch {
      return { module: 'pricing', configured: true, up: false, url: this.baseUrl };
    }
  }
}
