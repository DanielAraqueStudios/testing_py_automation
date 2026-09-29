export enum QuoteServiceType {
  WEB = 'WEB',
  SOCIAL = 'SOCIAL',
  BOT = 'BOT',
  FACEBOOK = 'FACEBOOK',
  AI = 'AI',
}

export interface QuoteServiceDto {
  type: QuoteServiceType;
  originalPrice: number;
  discountedPrice: number;
}

export interface CreateQuoteDto {
  clientId: string;
  paymentTerms?: string;
  services: QuoteServiceDto[];
}

export interface QuoteResponseDto {
  id: string;
  clientId: string;
  paymentTerms?: string;
  services: (QuoteServiceDto & { id: string })[];
  createdAt: string;
  updatedAt: string;
}
