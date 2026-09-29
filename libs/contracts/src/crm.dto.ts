export enum LeadStatus {
  NEW = 'NEW',
  CONTACTED = 'CONTACTED',
  QUALIFIED = 'QUALIFIED',
  LOST = 'LOST',
  CONVERTED = 'CONVERTED',
}

export enum DealStatus {
  PROSPECT = 'PROSPECT',
  IN_PROGRESS = 'IN_PROGRESS',
  ON_HOLD = 'ON_HOLD',
  COMPLETED = 'COMPLETED',
  CANCELLED = 'CANCELLED',
}

export interface LeadDto {
  id: string;
  contactId: string;
  source?: string;
  status: LeadStatus;
  createdAt: string;
  updatedAt: string;
}

export interface DealDto {
  id: string;
  leadId: string;
  title: string;
  status: DealStatus;
  progress: number;
  createdAt: string;
  updatedAt: string;
}
