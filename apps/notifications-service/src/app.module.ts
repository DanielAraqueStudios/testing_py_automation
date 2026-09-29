import { Module } from '@nestjs/common';
import { HealthController } from './health.controller';
import { ProgressGateway } from './progress.gateway';

@Module({
  imports: [],
  controllers: [HealthController],
  providers: [ProgressGateway],
})
export class AppModule {}
