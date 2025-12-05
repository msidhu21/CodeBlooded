'use client';

import React, { useState, useEffect, useMemo } from 'react';

interface CategoryTree {
  [parent: string]: string[]; // parent -> list of full category paths
}

export interface FilterState {
  query: string;
  category: string; // Keep for backward compatibility, will use categories array primarily
  categories: string[]; // New: support multiple categories
  minRating: string;
  maxRating: string;
  minPrice: string;
  maxPrice: string;
  minDiscount: string;
  compact: boolean;
}

interface SearchFiltersProps {
  filters: FilterState;
  onFiltersChange: (filters: FilterState) => void;
  onSearch: (filters?: FilterState) => void;
  categories: string[];
  isLoading?: boolean;
}

export default function SearchFilters({
  filters,
  onFiltersChange,
  onSearch,
  categories,
  isLoading = false,
}: SearchFiltersProps) {
  const [localFilters, setLocalFilters] = useState<FilterState>(filters);
  const [isOpen, setIsOpen] = useState(false);
  const [expandedParents, setExpandedParents] = useState<Set<string>>(new Set());

  useEffect(() => {
    setLocalFilters(filters);
  }, [filters]);

  // Parse categories into hierarchical structure
  const categoryTree = useMemo(() => {
    const tree: CategoryTree = {};
    categories.forEach(cat => {
      const parts = cat.split('|');
      if (parts.length > 0) {
        const parent = parts[0];
        if (!tree[parent]) {
          tree[parent] = [];
        }
        tree[parent].push(cat);
      }
    });
    return tree;
  }, [categories]);

  const parentCategories = useMemo(() => {
    return Object.keys(categoryTree).sort();
  }, [categoryTree]);

  const handleInputChange = (field: keyof FilterState, value: string | boolean) => {
    setLocalFilters({ ...localFilters, [field]: value });
  };

  const toggleParent = (parent: string) => {
    const newExpanded = new Set(expandedParents);
    if (newExpanded.has(parent)) {
      newExpanded.delete(parent);
    } else {
      newExpanded.add(parent);
    }
    setExpandedParents(newExpanded);
  };

  const handleCategoryToggle = (categoryPath: string, isParent: boolean) => {
    const currentCategories = localFilters.categories || [];
    
    if (isParent) {
      // If parent is clicked, toggle all its subcategories
      const parentCats = categoryTree[categoryPath] || [];
      const allSelected = parentCats.every((cat: string) => currentCategories.includes(cat));
      
      if (allSelected) {
        // Deselect all subcategories
        const newCategories = currentCategories.filter((cat: string) => !parentCats.includes(cat));
        setLocalFilters({ ...localFilters, categories: newCategories, category: '' });
      } else {
        // Select all subcategories
        const newCategories = [...new Set([...currentCategories, ...parentCats])];
        setLocalFilters({ ...localFilters, categories: newCategories, category: '' });
      }
    } else {
      // Toggle individual category
      if (currentCategories.includes(categoryPath)) {
        const newCategories = currentCategories.filter((cat: string) => cat !== categoryPath);
        setLocalFilters({ ...localFilters, categories: newCategories, category: '' });
      } else {
        const newCategories = [...currentCategories, categoryPath];
        setLocalFilters({ ...localFilters, categories: newCategories, category: '' });
      }
    }
  };

  const handleApplyFilters = () => {
    onFiltersChange(localFilters);
    onSearch(localFilters);
    setIsOpen(false);
  };

  const handleReset = () => {
    const resetFilters: FilterState = {
      query: '',
      category: '',
      categories: [],
      minRating: '',
      maxRating: '',
      minPrice: '',
      maxPrice: '',
      minDiscount: '',
      compact: false,
    };
    setLocalFilters(resetFilters);
    onFiltersChange(resetFilters);
    onSearch(resetFilters);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleApplyFilters();
    }
  };

  return (
    <>
      {/* Filter Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="btn btn-primary flex items-center gap-2"
        disabled={isLoading}
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
        </svg>
        Filters
      </button>

      {/* Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sliding Panel */}
      <div
        className={`fixed top-0 right-0 h-full w-full md:w-96 bg-white shadow-2xl z-50 transform transition-transform duration-300 ease-in-out overflow-y-auto ${
          isOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold">Search & Filters</h2>
            <button
              onClick={() => setIsOpen(false)}
              className="text-gray-500 hover:text-gray-700 text-3xl"
            >
              ×
            </button>
          </div>

      {/* Search Input */}
      <div className="mb-4">
        <label htmlFor="search" className="block text-sm font-medium mb-2">
          Search Products
        </label>
        <input
          id="search"
          type="text"
          value={localFilters.query}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange('query', e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Search by name, description, or category..."
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          disabled={isLoading}
        />
      </div>

      {/* Hierarchical Category Filter */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">
          Categories
          {localFilters.categories && localFilters.categories.length > 0 && (
            <span className="ml-2 text-xs text-gray-500">
              ({localFilters.categories.length} selected)
            </span>
          )}
        </label>
        <div className="border border-gray-300 rounded-lg max-h-64 overflow-y-auto">
          {parentCategories.length === 0 ? (
            <div className="p-4 text-gray-500 text-sm">No categories available</div>
          ) : (
            parentCategories.map((parent: string) => {
              const subcategories = categoryTree[parent] || [];
              const isExpanded = expandedParents.has(parent);
              const allSelected = subcategories.every((cat: string) => 
                localFilters.categories?.includes(cat)
              );
              const someSelected = subcategories.some((cat: string) => 
                localFilters.categories?.includes(cat)
              );

              return (
                <div key={parent} className="border-b border-gray-200 last:border-b-0">
                  {/* Parent Category */}
                  <div className="flex items-center p-3 hover:bg-gray-50">
                    <button
                      onClick={() => toggleParent(parent)}
                      className="mr-2 text-gray-600"
                      disabled={isLoading}
                    >
                      <svg
                        className={`w-4 h-4 transform transition-transform ${
                          isExpanded ? 'rotate-90' : ''
                        }`}
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </button>
                    <input
                      type="checkbox"
                      checked={allSelected}
                      onChange={() => handleCategoryToggle(parent, true)}
                      className="mr-2 w-4 h-4"
                      disabled={isLoading}
                      style={{
                        opacity: someSelected && !allSelected ? 0.5 : 1,
                      }}
                    />
                    <span className="text-sm font-medium flex-1">
                      {parent}
                      <span className="ml-2 text-xs text-gray-500">
                        ({subcategories.length})
                      </span>
                    </span>
                  </div>

                  {/* Subcategories */}
                  {isExpanded && (
                    <div className="pl-8 bg-gray-50">
                      {subcategories.map((cat: string) => {
                        const parts = cat.split('|');
                        const displayName = parts.slice(1).join(' > ') || cat;
                        const isSelected = localFilters.categories?.includes(cat);

                        return (
                          <div key={cat} className="flex items-center p-2 hover:bg-gray-100">
                            <input
                              type="checkbox"
                              checked={isSelected}
                              onChange={() => handleCategoryToggle(cat, false)}
                              className="mr-2 w-4 h-4"
                              disabled={isLoading}
                            />
                            <span className="text-sm text-gray-700">{displayName}</span>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Rating Filters */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label htmlFor="minRating" className="block text-sm font-medium mb-2">
            Min Rating
          </label>
          <input
            id="minRating"
            type="number"
            min="0"
            max="5"
            step="0.1"
            value={localFilters.minRating}
            onChange={(e) => handleInputChange('minRating', e.target.value)}
            placeholder="0.0"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            disabled={isLoading}
          />
        </div>
        <div>
          <label htmlFor="maxRating" className="block text-sm font-medium mb-2">
            Max Rating
          </label>
          <input
            id="maxRating"
            type="number"
            min="0"
            max="5"
            step="0.1"
            value={localFilters.maxRating}
            onChange={(e) => handleInputChange('maxRating', e.target.value)}
            placeholder="5.0"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            disabled={isLoading}
          />
        </div>
      </div>

      {/* Price Filters */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label htmlFor="minPrice" className="block text-sm font-medium mb-2">
            Min Price (₹)
          </label>
          <input
            id="minPrice"
            type="number"
            min="0"
            step="1"
            value={localFilters.minPrice}
            onChange={(e) => handleInputChange('minPrice', e.target.value)}
            placeholder="0"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            disabled={isLoading}
          />
        </div>
        <div>
          <label htmlFor="maxPrice" className="block text-sm font-medium mb-2">
            Max Price (₹)
          </label>
          <input
            id="maxPrice"
            type="number"
            min="0"
            step="1"
            value={localFilters.maxPrice}
            onChange={(e) => handleInputChange('maxPrice', e.target.value)}
            placeholder="No limit"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            disabled={isLoading}
          />
        </div>
      </div>

      {/* Discount Filter */}
      <div className="mb-4">
        <label htmlFor="minDiscount" className="block text-sm font-medium mb-2">
          Min Discount (%)
        </label>
        <input
          id="minDiscount"
          type="number"
          min="0"
          max="100"
          step="1"
          value={localFilters.minDiscount}
          onChange={(e) => handleInputChange('minDiscount', e.target.value)}
          placeholder="0"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          disabled={isLoading}
        />
      </div>

      {/* Compact View Toggle */}
      <div className="mb-6">
        <label className="flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={localFilters.compact}
            onChange={(e) => handleInputChange('compact', e.target.checked)}
            className="mr-2 w-4 h-4"
            disabled={isLoading}
          />
          <span className="text-sm font-medium">Compact View (Hide Descriptions)</span>
        </label>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3">
        <button
          onClick={handleApplyFilters}
          disabled={isLoading}
          className="btn btn-primary flex-1"
        >
          {isLoading ? 'Searching...' : 'Apply Filters'}
        </button>
        <button
          onClick={handleReset}
          disabled={isLoading}
          className="btn flex-1"
        >
          Reset
        </button>
      </div>
        </div>
      </div>
    </>
  );
}
