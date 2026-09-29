import { Module } from '@nestjs/common';
import { Queue } from 'bullmq';

// TODO: wire a real Redis connection (host/port from env) once infra is provisioned.
export const CAMPAIGNS_QUEUE = 'campaigns-queue';

@Module({
  providers: [
    {
      provide: CAMPAIGNS_QUEUE,
      useFactory: () =>
        new Queue(CAMPAIGNS_QUEUE, {
          connection: { host: 'localhost', port: 6379 },
        }),
    },
  ],
  exports: [CAMPAIGNS_QUEUE],
})
export class CampaignsQueueModule {}
