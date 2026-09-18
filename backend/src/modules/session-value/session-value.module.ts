import { Module } from '@nestjs/common';
import { SessionValueController } from './session-value.controller';
import { SessionValueService } from './session-value.service';

@Module({
  controllers: [SessionValueController],
  providers: [SessionValueService],
  exports: [SessionValueService],
})
export class SessionValueModule {}
