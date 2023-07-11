export type HttpUrl = string;

export const isHttpUrl = (value: any): value is HttpUrl => {
  try {
    const url = new URL(value);
    return url.protocol === 'http:' || url.protocol === 'https:';
  } catch {
    return false;
  }
};

export type Uuid4 = string;

export const isUuid4 = (value: any): value is Uuid4 => {
  const uuid4Pattern =
    /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$/;
  return typeof value === 'string' && uuid4Pattern.test(value);
};

export type Iso8601 = string;

export const isIso8601 = (value: string): boolean => {
  const iso8601Pattern =
    /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(\.\d+)?(([+-]\d{2}:\d{2})|Z)?$/;
  return iso8601Pattern.test(value);
};

export type UnsignedInteger = number;

export const isUnsignedInteger = (value: any): value is UnsignedInteger => {
  return typeof value === 'number' && Number.isInteger(value) && value >= 0;
};
