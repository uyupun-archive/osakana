import axios from 'axios';
import { AxiosError } from 'axios';
import { StatusCodes } from 'http-status-codes';

import type { Uuid4, HttpUrl, ReadingList, ReadingListRecord } from '../../types';
import type { ReadingListRecordResponse } from '../types';
import { isUuid4, isHttpUrl } from '../../types';
import { isValidReadingListRecordResponse } from '../types';
import { UnknownError, InvalidUuid4Error, InvalidHttpUrlError } from '../../errors';
import { ReadingListRecordTypeError, UrlNotFoundError, UrlAlreadyExistsError } from '../errors';

export const addReadingListRecord = async (url: HttpUrl): Promise<void> => {
  if (!isHttpUrl(url)) {
    throw new InvalidHttpUrlError();
  }
  try {
    await axios.post('/api/reading-list', {url});
  } catch (e: unknown) {
    if (e instanceof AxiosError) {
      if (e.response?.status === StatusCodes.NOT_FOUND) {
        throw new UrlNotFoundError();
      }
      if (e.response?.status === StatusCodes.CONFLICT) {
        throw new UrlAlreadyExistsError();
      }
      throw new UnknownError();
    }
    throw new UnknownError();
  }
};

export const searchReadingList = async (keyword: string): Promise<ReadingList> => {
  const res = await axios.get('/api/reading-list', {params: {keyword}});

  if (Array.isArray(res.data) && res.data.every(isValidReadingListRecordResponse)) {
    return res.data.map(_parseReadingListRecord);
  }
  throw new ReadingListRecordTypeError();
};

export const fetchFeelingReadingListRecord = async (): Promise<ReadingListRecord> => {
  const res = await axios.get('/api/reading-list/feeling');

  if (isValidReadingListRecordResponse(res.data)) {
    return _parseReadingListRecord(res.data);
  }
  throw new ReadingListRecordTypeError();
};

export const readReadingListRecord = async (id: Uuid4): Promise<void> => {
  if (!isUuid4(id)) {
    throw new InvalidUuid4Error();
  }
  await axios.patch('/api/reading-list/read', {id});
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