import { Module } from '@nestjs/common';

// One module per student team. Each team owns exactly one folder.
// Uncomment a module once that team's code is ready to integrate.
import { SkillsGapModule } from './modules/skills-gap/skills-gap.module';
import { CareerPathModule } from './modules/career-path/career-path.module';
import { MatchingModule } from './modules/matching/matching.module';
import { ChatbotModule } from './modules/chatbot/chatbot.module';
import { SessionValueModule } from './modules/session-value/session-value.module';
import { PricingModule } from './modules/pricing/pricing.module';
import { AnalyticsModule } from './modules/analytics/analytics.module';
import { MicroLearningModule } from './modules/micro-learning/micro-learning.module';

@Module({
  imports: [
    SkillsGapModule,      // U-CS 3  — the spine, feeds 1 and 8
    CareerPathModule,     // U-CS 1
    MatchingModule,       // U-CS 2
    ChatbotModule,        // U-CS 4
    SessionValueModule,   // U-CS 5
    PricingModule,        // U-CS 6
    AnalyticsModule,      // U-CS 7  — unassigned, spare
    MicroLearningModule,  // U-CS 8
  ],
})
export class AppModule {}
