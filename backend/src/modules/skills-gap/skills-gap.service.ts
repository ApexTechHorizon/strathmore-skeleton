import { HttpException, Injectable, Logger } from '@nestjs/common';
import { SkillsGapRequestDto, SkillsGapResponseDto } from './dto/skills-gap.dto';

/**
 * U-CS 3 — adapter for the service built by the assigned team.
 *
 * We do not implement the logic. We call their hosted URL and pass the answer on.
 * Free hosting sleeps, so the first call after a quiet period can be slow — hence
 * the generous timeout.
 */
@Injectable()
export class SkillsGapService {
  private readonly log = new Logger(SkillsGapService.name);
  private readonly baseUrl = process.env.SKILLS_GAP_SERVICE_URL ?? '';
  private readonly timeoutMs = Number(process.env.STUDENT_SERVICE_TIMEOUT_MS ?? 30000);

  async call(body: SkillsGapRequestDto): Promise<SkillsGapResponseDto> {
    if (!this.baseUrl) {
      throw new HttpException('skills-gap: SKILLS_GAP_SERVICE_URL is not set — no service URL yet', 503);
    }

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const res = await fetch(`${this.baseUrl}/gap`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      if (!res.ok) {
        throw new HttpException(`skills-gap: upstream returned ${res.status}`, 502);
      }
      return (await res.json()) as SkillsGapResponseDto;
    } catch (err) {
      this.log.error(`skills-gap upstream failed: ${err}`);
      throw new HttpException('skills-gap: upstream unavailable', 502);
    } finally {
      clearTimeout(timer);
    }
  }

  async status() {
    if (!this.baseUrl) return { module: 'skills-gap', configured: false };
    try {
      const res = await fetch(`${this.baseUrl}/health`);
      return { module: 'skills-gap', configured: true, up: res.ok, url: this.baseUrl };
    } catch {
      return { module: 'skills-gap', configured: true, up: false, url: this.baseUrl };
    }
  }
}
