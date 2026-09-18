import { Body, Controller, Get, Post } from '@nestjs/common';
import { SkillsGapService } from './skills-gap.service';
import { SkillsGapRequestDto, SkillsGapResponseDto } from './dto/skills-gap.dto';

/**
 * U-CS 3 — Skills Gap & Trust Scoring
 * Built and hosted by: the assigned team
 *
 * This is an ADAPTER. The logic lives in their service; we call it.
 * Their URL is configured as SKILLS_GAP_SERVICE_URL.
 */
@Controller('skills-gap')
export class SkillsGapController {
  constructor(private readonly service: SkillsGapService) {}

  @Post('gap')
  async handle(@Body() body: SkillsGapRequestDto): Promise<SkillsGapResponseDto> {
    return this.service.call(body);
  }

  /** Is their service up? Useful before a demo. */
  @Get('status')
  async status() {
    return this.service.status();
  }
}
