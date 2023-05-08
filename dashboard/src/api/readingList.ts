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
    ...record,
    created_at: new Date(record.created_at),
    updated_at: new Date(record.updated_at),
    read_at: record.read_at ? new Date(record.read_at) : null,
  }));
  return readingList;
};
