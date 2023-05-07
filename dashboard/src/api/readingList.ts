import axios from 'axios';

import { ReadingList } from '../types';

export const searchReadingList = async (keyword: string): Promise<ReadingList> => {
  const res = await axios.get('/api/reading-list', {
    params: {
      keyword
    },
  });
  return res.data;
};
