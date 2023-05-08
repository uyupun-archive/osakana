import type { Uuid, HttpUrl } from './common';
import { isUuid4, isHttpUrl, isIso8601 } from '../types/common';

export interface ReadingListSearchParams {
  keyword: string;
}

export interface ReadingListRecordResponse {
  id: Uuid;
  url: HttpUrl;
  title: string;
  is_read: boolean;
  thumb: HttpUrl | null;
  created_at: string;
  updated_at: string;
  read_at: string | null;
};

export const isValidReadingListRecordResponse = (record: any): record is ReadingListRecordResponse => {
  return (
    isUuid4(record.id) &&
    isHttpUrl(record.url) &&
    typeof record.title === 'string' &&
    typeof record.is_read === 'boolean' &&
    (record.thumb === null || isHttpUrl(record.thumb)) &&
    isIso8601(record.created_at) &&
    isIso8601(record.updated_at) &&
    (record.read_at === null || isIso8601(record.read_at))
  );
};

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
