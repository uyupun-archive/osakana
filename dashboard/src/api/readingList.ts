import axios from 'axios';
import { AxiosError } from 'axios';

import type { HttpUrl, ReadingList, ReadingListRecord } from '../types';
import type { ReadingListRecordResponse } from './types';
import { isHttpUrl } from '../types';
import { isValidReadingListRecordResponse } from './types';
import { UnknownError, InvalidHttpUrlError } from '../errors';
import { ReadingListRecordTypeError, UrlNotFoundError, UrlAlreadyExistsError } from './errors';

export const searchReadingList = async (keyword: string): Promise<ReadingList> => {
  const res = await axios.get('/api/reading-list', {
    params: {
      keyword
    }
  });

  if (Array.isArray(res.data) && res.data.every(isValidReadingListRecordResponse)) {
    return res.data.map(_parseReadingListRecord);
  }
  throw new ReadingListRecordTypeError();
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

export const addReadingListRecord = async (url: HttpUrl): Promise<void> => {
  if (!isHttpUrl(url)) {
    throw new InvalidHttpUrlError();
  }
  try {
    await axios.post('/api/reading-list', {
      url
    });
  } catch (e: unknown) {
    if (e instanceof AxiosError) {
      if (e.response?.status === 404) {
        throw new UrlNotFoundError();
      }
      if (e.response?.status === 409) {
        throw new UrlAlreadyExistsError();
      }
      throw new UnknownError();
    }
    throw new UnknownError();
  }
}
