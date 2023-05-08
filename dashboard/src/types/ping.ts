export interface PingResponse {
  message: 'pong';
};

export const isValidPingResponse = (res: any): res is PingResponse => {
  return res.message === 'pong';
};
