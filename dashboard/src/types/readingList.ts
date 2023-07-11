import { isUnsignedInteger, type Uuid4, type HttpUrl, type UnsignedInteger } from './common';

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
}

export type ReadingList = ReadingListRecord[];

export interface ReadingListSearchFilters {
  is_bookmarked?: boolean;
  is_read?: boolean;
  is_unread?: boolean;
}

export interface ReadingListCounts {
  total: UnsignedInteger;
  reads: UnsignedInteger;
  unreads: UnsignedInteger;
  bookmarks: UnsignedInteger;
}

export const isValidReadingListCounts = (counts: any): counts is ReadingListCounts => {
  return (
    isUnsignedInteger(counts.total) &&
    isUnsignedInteger(counts.reads) &&
    isUnsignedInteger(counts.unreads) &&
    isUnsignedInteger(counts.bookmarks)
  );
};

export interface ExportReadingListRecord extends ReadingListRecord {
  title_bigrams: string[];
  title_trigrams: string[];
  title_morphemes: string[];
}

export type ExportReadingList = ExportReadingListRecord[];
