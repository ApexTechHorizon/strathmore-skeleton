import { Module } from '@nestjs/common';
import { CareerPathController } from './career-path.controller';
import { CareerPathService } from './career-path.service';

@Module({
  controllers: [CareerPathController],
  providers: [CareerPathService],
  exports: [CareerPathService],
})
export class CareerPathModule {}
