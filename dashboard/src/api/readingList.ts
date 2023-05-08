import axios from 'axios';

import { ReadingList, ReadingListRecord } from '../types';

export const searchReadingList = async (keyword: string): Promise<ReadingList> => {
  const res = await axios.get('/api/reading-list', {
    params: {
      keyword
    },
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
