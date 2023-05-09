import type { Uuid4, HttpUrl } from './common';

export interface ReadingListRecord {
  id: Uuid4;
  url: HttpUrl;
  title: string;
  isRead: boolean;
  isBookmarked: boolean;
  thumb: HttpUrl | null;
  createdAt: Date;
  updatedAt: Date;
  readAt: Date | null;
  bookmarkedAt: Date | null;
};

export type ReadingList = Array<ReadingListRecord>;
