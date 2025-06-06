export const countUniqueWords = (text) => {
  if (!text) return 0;
  const words = text.trim().split(/\s+/).map(word => word.toLowerCase());
  const uniqueWords = new Set(words);
  return uniqueWords.size;
};

