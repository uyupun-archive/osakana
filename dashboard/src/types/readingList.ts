import { UUID, HttpUrl } from "./common";

export interface ReadingListRecord {
  id: UUID;
  url: HttpUrl;
  title: string;
  is_read: boolean;
  thumb: HttpUrl | null;
  created_at: Date;
  updated_at: Date;
  read_at: Date;
};

export type ReadingList = Array<ReadingListRecord>;
