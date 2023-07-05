import axios, { AxiosError } from 'axios';
import { StatusCodes } from 'http-status-codes';

import { UnknownError, InvalidUuid4Error, InvalidHttpUrlError } from '../../errors';
import {
  isUuid4,
  isHttpUrl,
  isValidReadingListCounts,
  type Uuid4,
  type HttpUrl,
  type ReadingList,
  type ReadingListRecord,
  type ReadingListSearchFilters,
  type ReadingListCounts,
  type ExportReadingListRecord,
  type ExportReadingList,
} from '../../types';
import {
  ValidationError,
  UrlNotFoundError,
  UrlAlreadyExistsError,
  ReadingListRecordTypeError,
  ReadingListRecordNotFoundError,
  ReadingListRecordAlreadyReadError,
  ReadingListRecordNotYetReadError,
  ReadingListCountsTypeError,
  ExportReadingListRecordTypeError,
  EmptyFileError,
  FileSizeLimitExceededError,
  InvalidFileExtensionError,
  InvalidJsonContentsError,
  InvalidJsonStructureError,
  ExportReadingListRecordParseError,
  ReadingListRecordDuplicateError,
} from '../errors';
import {
  isValidReadingListRecordResponse,
  isValidExportReadingListRecordResponse,
  type ReadingListRecordResponse,
  type ExportReadingListRecordResponse,
} from '../types';

const apiUrl = import.meta.env.VITE_API_URL;

export const addReadingListRecord = async (url: HttpUrl): Promise<void> => {
  if (!isHttpUrl(url)) {
    throw new InvalidHttpUrlError();
  }
  try {
    await axios.post(`${apiUrl}/api/reading-list`, { url });
  } catch (e: unknown) {
    if (e instanceof AxiosError) {
      if (e.response?.status === StatusCodes.UNPROCESSABLE_ENTITY) {
        throw new ValidationError();
      }
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

export const searchReadingList = async (
  keyword: string,
  filters: ReadingListSearchFilters
): Promise<ReadingList> => {
  let res;
  try {
    res = await axios.get<ReadingListRecordResponse[]>(`${apiUrl}/api/reading-list`, {
      params: { keyword, ...filters },
    });
  } catch (e: unknown) {
    if (e instanceof AxiosError) {
      if (e.response?.status === StatusCodes.UNPROCESSABLE_ENTITY) {
        throw new ValidationError();
      }
      throw new UnknownError();
    }
    throw new UnknownError();
  }

  if (Array.isArray(res.data) && res.data.every(isValidReadingListRecordResponse)) {
    return res.data.map(_parseReadingListRecord);
  }
  throw new ReadingListRecordTypeError();
};

export const fishingReadingListRecord = async (): Promise<ReadingListRecord> => {
  const res = await axios.get<ReadingListRecordResponse>(`${apiUrl}/api/reading-list/fishing`);

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
      if (e.response?.status === StatusCodes.UNPROCESSABLE_ENTITY) {
        throw new ValidationError();
      }
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
      if (e.response?.status === StatusCodes.UNPROCESSABLE_ENTITY) {
        throw new ValidationError();
      }
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
      if (e.response?.status === StatusCodes.UNPROCESSABLE_ENTITY) {
        throw new ValidationError();
      }
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
      if (e.response?.status === StatusCodes.UNPROCESSABLE_ENTITY) {
        throw new ValidationError();
      }
      if (e.response?.status === StatusCodes.NOT_FOUND) {
        throw new ReadingListRecordNotFoundError();
      }
      throw new UnknownError();
    }
    throw new UnknownError();
  }
};

export const getReadingListCounts = async (): Promise<ReadingListCounts> => {
  const res = await axios.get<ReadingListCounts>(`${apiUrl}/api/reading-list/counts`);
  if (isValidReadingListCounts(res.data)) {
    return res.data;
  }
  throw new ReadingListCountsTypeError();
};

export const exportReadingList = async (): Promise<ExportReadingList> => {
  const res = await axios.get<ExportReadingListRecordResponse[]>(
    `${apiUrl}/api/reading-list/export`
  );
  if (Array.isArray(res.data) && res.data.every(isValidExportReadingListRecordResponse)) {
    return res.data.map(_parseExportReadingListRecord);
  }
  throw new ExportReadingListRecordTypeError();
};

export const importReadingList = async (formData: FormData): Promise<void> => {
  try {
    await axios.post(`${apiUrl}/api/reading-list/import`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  } catch (e: unknown) {
    if (e instanceof AxiosError) {
      if (e.response?.status === StatusCodes.BAD_REQUEST) {
        if (e.response.data.message === 'Empty file') {
          throw new EmptyFileError();
        }
        if (e.response.data.message === 'Invalid json contents') {
          throw new InvalidJsonContentsError();
        }
        if (e.response.data.message === 'Invalid json structure') {
          throw new InvalidJsonStructureError();
        }
        throw new UnknownError();
      }
      if (e.response?.status === StatusCodes.CONFLICT) {
        throw new ReadingListRecordDuplicateError();
      }
      if (e.response?.status === StatusCodes.REQUEST_TOO_LONG) {
        throw new FileSizeLimitExceededError();
      }
      if (e.response?.status === StatusCodes.UNSUPPORTED_MEDIA_TYPE) {
        throw new InvalidFileExtensionError();
      }
      if (e.response?.status === StatusCodes.UNPROCESSABLE_ENTITY) {
        throw new ExportReadingListRecordParseError();
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
    readAt: record.read_at !== null ? new Date(record.read_at) : null,
    bookmarkedAt: record.bookmarked_at !== null ? new Date(record.bookmarked_at) : null,
  };
};

const _parseExportReadingListRecord = (
  record: ExportReadingListRecordResponse
): ExportReadingListRecord => {
  const baseRecord = _parseReadingListRecord(record);
  return {
    ...baseRecord,
    title_bigrams: record.title_bigrams,
    title_trigrams: record.title_trigrams,
    title_morphemes: record.title_morphemes,
  };
};
