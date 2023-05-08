export interface PingResponse {
  message: string;
};

export const isValidPingResponse = (record: any): record is PingResponse => {
  return typeof record.message === 'string';
};
