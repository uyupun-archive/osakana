import { UUID, HttpUrl } from "./common";

export interface ReadingListRecord {
  id: UUID;
  url: HttpUrl;
  title: string;
  isRead: boolean;
  thumb: HttpUrl | null;
  createdAt: Date;
  updatedAt: Date;
  readAt: Date | null;
};

export type ReadingList = Array<ReadingListRecord>;
