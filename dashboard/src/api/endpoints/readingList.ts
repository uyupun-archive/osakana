import axios from 'axios';
import { AxiosError } from 'axios';
import { StatusCodes } from 'http-status-codes';

import type { Uuid4, HttpUrl, ReadingList, ReadingListRecord } from '../../types';
import type { ReadingListRecordResponse } from '../types';
import { isUuid4, isHttpUrl } from '../../types';
import { isValidReadingListRecordResponse } from '../types';
import { UnknownError, InvalidUuid4Error, InvalidHttpUrlError } from '../../errors';
import {
  UrlNotFoundError,
  UrlAlreadyExistsError,
  ReadingListRecordTypeError,
  ReadingListRecordNotFoundError,
  ReadingListRecordAlreadyReadError,
  ReadingListRecordNotYetReadError
} from '../errors';

const apiUrl = import.meta.env.VITE_API_URL;

export const addReadingListRecord = async (url: HttpUrl): Promise<void> => {
  if (!isHttpUrl(url)) {
    throw new InvalidHttpUrlError();
  }
  try {
    await axios.post(`${apiUrl}/api/reading-list`, {url});
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
  const res = await axios.get(`${apiUrl}/api/reading-list`, {params: {keyword}});

  if (Array.isArray(res.data) && res.data.every(isValidReadingListRecordResponse)) {
    return res.data.map(_parseReadingListRecord);
  }
  throw new ReadingListRecordTypeError();
};

export const fetchFeelingReadingListRecord = async (): Promise<ReadingListRecord> => {
  const res = await axios.get(`${apiUrl}/api/reading-list/feeling`);

  if (isValidReadingListRecordResponse(res.data)) {
    return _parseReadingListRecord(res.data);
  }
  throw new ReadingListRecordTypeError();
};

export const readReadingListRecord = async (id: Uuid4): Promise<void> => {
  if (!isUuid4(id)) {
    throw new InvalidUuid4Error();
  }
  try {
    await axios.patch(`${apiUrl}/api/reading-list/read/${id}`);
  } catch (e: unknown) {
    if (e instanceof AxiosError) {
      if (e.response?.status === StatusCodes.NOT_FOUND) {
        throw new ReadingListRecordNotFoundError();
      }
      if (e.response?.status === StatusCodes.FORBIDDEN) {
        throw new ReadingListRecordAlreadyReadError();
      }
      throw new UnknownError();
    }
    throw new UnknownError();
  }
};

export const unreadReadingListRecord = async (id: Uuid4): Promise<void> => {
  if (!isUuid4(id)) {
    throw new InvalidUuid4Error();
  }
  try {
    await axios.patch(`${apiUrl}/api/reading-list/unread/${id}`);
  } catch (e: unknown) {
    if (e instanceof AxiosError) {
      if (e.response?.status === StatusCodes.NOT_FOUND) {
        throw new ReadingListRecordNotFoundError();
      }
      if (e.response?.status === StatusCodes.FORBIDDEN) {
        throw new ReadingListRecordNotYetReadError();
      }
      throw new UnknownError();
    }
    throw new UnknownError();
  }
};

export const deleteReadingListRecord = async (id: Uuid4): Promise<void> => {
  if (!isUuid4(id)) {
    throw new InvalidUuid4Error();
  }
  try {
    await axios.delete(`${apiUrl}/api/reading-list/${id}`);
  } catch (e: unknown) {
    if (e instanceof AxiosError) {
      if (e.response?.status === StatusCodes.NOT_FOUND) {
        throw new ReadingListRecordNotFoundError();
      }
      throw new UnknownError();
    }
    throw new UnknownError();
  }
};

export const bookmarkReadingListRecord = async (id: Uuid4): Promise<void> => {
  if (!isUuid4(id)) {
    throw new InvalidUuid4Error();
  }
  try {
    await axios.patch(`${apiUrl}/api/reading-list/bookmark/${id}`);
  } catch (e: unknown) {
    if (e instanceof AxiosError) {
      if (e.response?.status === StatusCodes.NOT_FOUND) {
        throw new ReadingListRecordNotFoundError();
      }
      throw new UnknownError();
    }
    throw new UnknownError();
  }
};

const _parseReadingListRecord = (record: ReadingListRecordResponse): ReadingListRecord => {
  return {
    id: record.id,
    url: record.url,
    title: record.title,
    isRead: record.is_read,
    isBookmarked: record.is_bookmarked,
    thumb: record.thumb,
    createdAt: new Date(record.created_at),
    updatedAt: new Date(record.updated_at),
    readAt: record.read_at ? new Date(record.read_at) : null,
    bookmarkedAt: record.bookmarked_at ? new Date(record.bookmarked_at) : null,
  };
};
