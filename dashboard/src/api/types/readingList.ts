import { isUuid4, isHttpUrl, isIso8601, type Uuid4, type HttpUrl, type Iso8601 } from '../../types';

export interface ReadingListRecordResponse {
  id: Uuid4;
  url: HttpUrl;
  title: string;
  is_read: boolean;
  is_bookmarked: boolean;
  thumb: HttpUrl | null;
  created_at: Iso8601;
  updated_at: Iso8601;
  read_at: Iso8601 | null;
  bookmarked_at: Iso8601 | null;
}

export const isValidReadingListRecordResponse = (
  record: any
): record is ReadingListRecordResponse => {
  return (
    isUuid4(record.id) &&
    isHttpUrl(record.url) &&
    typeof record.title === 'string' &&
    typeof record.is_read === 'boolean' &&
    typeof record.is_bookmarked === 'boolean' &&
    (record.thumb === null || isHttpUrl(record.thumb)) &&
    isIso8601(record.created_at) &&
    isIso8601(record.updated_at) &&
    (record.read_at === null || isIso8601(record.read_at)) &&
    (record.bookmarked_at === null || isIso8601(record.bookmarked_at))
  );
};

export interface ExportReadingListRecordResponse extends ReadingListRecordResponse {
  title_bigrams: string[];
  title_trigrams: string[];
  title_morphemes: string[];
}

export const isValidExportReadingListRecordResponse = (
  record: any
): record is ExportReadingListRecordResponse => {
  return (
    isValidReadingListRecordResponse(record as ReadingListRecordResponse) &&
    Array.isArray(record.title_bigrams) &&
    (record.title_bigrams as any[]).every((bigram: any) => typeof bigram === 'string') &&
    Array.isArray(record.title_trigrams) &&
    (record.title_trigrams as any[]).every((trigram: any) => typeof trigram === 'string') &&
    Array.isArray(record.title_morphemes) &&
    (record.title_morphemes as any[]).every((morpheme: any) => typeof morpheme === 'string')
  );
};
