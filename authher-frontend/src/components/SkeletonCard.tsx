const SkeletonCard = () => {
  return (
    <div className="animate-pulse rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4 space-y-3 shadow">
      <div className="h-4 w-3/4 bg-gray-300 dark:bg-gray-600 rounded" />
      <div className="h-3 w-1/2 bg-gray-200 dark:bg-gray-700 rounded" />
      <div className="h-3 w-1/4 bg-gray-200 dark:bg-gray-700 rounded" />
      <div className="h-3 w-1/3 bg-gray-300 dark:bg-gray-600 rounded" />
      <div className="h-4 w-full bg-gray-200 dark:bg-gray-700 rounded" />
      <div className="h-4 w-5/6 bg-gray-200 dark:bg-gray-700 rounded" />
    </div>
  );
};

export default SkeletonCard;
