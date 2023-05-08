import type { Uuid, HttpUrl } from './common';

export interface ReadingListRecord {
  id: Uuid;
  url: HttpUrl;
  title: string;
  isRead: boolean;
  thumb: HttpUrl | null;
  createdAt: Date;
  updatedAt: Date;
  readAt: Date | null;
};

export type ReadingList = Array<ReadingListRecord>;
