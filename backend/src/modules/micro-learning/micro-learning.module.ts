import { Module } from '@nestjs/common';
import { MicroLearningController } from './micro-learning.controller';
import { MicroLearningService } from './micro-learning.service';

@Module({
  controllers: [MicroLearningController],
  providers: [MicroLearningService],
  exports: [MicroLearningService],
})
export class MicroLearningModule {}
