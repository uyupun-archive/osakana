import axios from 'axios';

import type { ReadingList, ReadingListRecord, ReadingListRecordResponse, ReadingListSearchParams } from '../types';
import { isValidReadingListRecordResponse } from '../types';

export const searchReadingList = async (params: ReadingListSearchParams): Promise<ReadingList> => {
  const res = await axios.get('/api/reading-list', {
    params: params
  });

  if (Array.isArray(res.data) && res.data.every(isValidReadingListRecordResponse)) {
    return res.data.map(_parseReadingListRecord);
  }
  throw new Error('Invalid response');
};

const _parseReadingListRecord = (record: ReadingListRecordResponse): ReadingListRecord => {
  return {
    id: record.id,
    url: record.url,
    title: record.title,
    isRead: record.is_read,
    thumb: record.thumb,
    createdAt: new Date(record.created_at),
    updatedAt: new Date(record.updated_at),
    readAt: record.read_at ? new Date(record.read_at) : null,
  };
};
