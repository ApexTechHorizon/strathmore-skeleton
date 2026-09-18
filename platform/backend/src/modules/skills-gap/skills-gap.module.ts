import { Module } from '@nestjs/common';
import { SkillsGapController } from './skills-gap.controller';
import { SkillsGapService } from './skills-gap.service';

@Module({
  controllers: [SkillsGapController],
  providers: [SkillsGapService],
  exports: [SkillsGapService],
})
export class SkillsGapModule {}
