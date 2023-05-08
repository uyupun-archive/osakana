import axios from 'axios';

import type { PingResponse } from '../types';
import { isValidPingResponse } from '../types';
import { PingTypeError } from '../errors';

export const ping = async (): Promise<PingResponse> => {
  const res = await axios.get('/api/ping');
  if (isValidPingResponse(res.data)) {
    return res.data;
  }
  throw new PingTypeError();
};
