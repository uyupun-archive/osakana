import type { Uuid4, HttpUrl, UnsignedInteger } from './common';
import { isUnsignedInteger } from './common';

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
  total: UnsignedInteger;
  reads: UnsignedInteger;
  unreads: UnsignedInteger;
  bookmarks: UnsignedInteger;
};

export const isValidReadingListCounts = (counts: any): counts is ReadingListCounts => {
  return (
    isUnsignedInteger(counts.total) &&
    isUnsignedInteger(counts.reads) &&
    isUnsignedInteger(counts.unreads) &&
    isUnsignedInteger(counts.bookmarks)
  );
};
