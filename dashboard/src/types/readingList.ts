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

export interface ReadingListSearchFilters {
  is_bookmarked?: boolean;
  is_read?: boolean;
  is_unread?: boolean;
};

export interface ReadingListCounts {
  total: number;
  reads: number;
  unreads: number;
  bookmarks: number;
};

export const isValidReadingListCounts = (counts: any): counts is ReadingListCounts => {
  return (
    typeof counts.total === 'number' &&
    typeof counts.reads === 'number' &&
    typeof counts.unreads === 'number' &&
    typeof counts.bookmarks === 'number'
  );
};
