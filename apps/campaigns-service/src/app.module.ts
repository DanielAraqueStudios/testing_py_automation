import { Module } from '@nestjs/common';
import { HealthController } from './health.controller';
import { PrismaService } from './prisma.service';
import { CampaignsQueueModule } from './campaigns-queue.module';

@Module({
  imports: [CampaignsQueueModule],
  controllers: [HealthController],
  providers: [PrismaService],
})
export class AppModule {}
