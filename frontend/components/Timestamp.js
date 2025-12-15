'use client';

export default function Timestamp({ date }) {
  const time = new Date(date).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });

  return <span>{time}</span>;
}
