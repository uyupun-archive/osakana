import axios from 'axios';

import { ReadingList, ReadingListRecord, ReadingListSearchParams } from '../types';

export const searchReadingList = async (params: ReadingListSearchParams): Promise<ReadingList> => {
  const res = await axios.get('/api/reading-list', {
    params: params
  });
  return _parseReadingList(res.data);
};

const _parseReadingList = (data: any): ReadingList => {
  const readingList = data.map((record: any): ReadingListRecord => ({
    id: record.id,
    url: record.url,
    title: record.title,
    isRead: record.is_read,
    thumb: record.thumb,
    createdAt: new Date(record.created_at),
    updatedAt: new Date(record.updated_at),
    readAt: record.read_at ? new Date(record.read_at) : null,
  }));
  return readingList;
};
