import { Product, Category, RepairRequest } from '@/types/product';

export const categories: Category[] = [
  {
    id: '1',
    name: 'Computers',
    slug: 'computers',
    description: 'Desktop computers and workstations',
    image: 'https://images.pexels.com/photos/2582937/pexels-photo-2582937.jpeg?auto=compress&cs=tinysrgb&w=400',
    isActive: true,
    sortOrder: 1,
    subcategories: [
      { id: '1-1', name: 'Desktop PCs', slug: 'desktop-pcs', isActive: true, sortOrder: 1 },
      { id: '1-2', name: 'All-in-One PCs', slug: 'all-in-one-pcs', isActive: true, sortOrder: 2 },
      { id: '1-3', name: 'Gaming PCs', slug: 'gaming-pcs', isActive: true, sortOrder: 3 },
      { id: '1-4', name: 'Workstations', slug: 'workstations', isActive: true, sortOrder: 4 },
    ]
  },
  {
    id: '2',
    name: 'Laptops',
    slug: 'laptops',
    description: 'Portable computing solutions',
    image: 'https://images.pexels.com/photos/18105/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=400',
    isActive: true,
    sortOrder: 2,
    subcategories: [
      { id: '2-1', name: 'Business Laptops', slug: 'business-laptops', isActive: true, sortOrder: 1 },
      { id: '2-2', name: 'Gaming Laptops', slug: 'gaming-laptops', isActive: true, sortOrder: 2 },
      { id: '2-3', name: 'Ultrabooks', slug: 'ultrabooks', isActive: true, sortOrder: 3 },
      { id: '2-4', name: 'Budget Laptops', slug: 'budget-laptops', isActive: true, sortOrder: 4 },
    ]
  },
  {
    id: '3',
    name: 'Phones',
    slug: 'phones',
    description: 'Latest smartphones and tablets',
    image: 'https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg?auto=compress&cs=tinysrgb&w=400',
    isActive: true,
    sortOrder: 3,
    subcategories: [
      { id: '3-1', name: 'Smartphones', slug: 'smartphones', isActive: true, sortOrder: 1 },
      { id: '3-2', name: 'Tablets', slug: 'tablets', isActive: true, sortOrder: 2 },
      { id: '3-3', name: 'Feature Phones', slug: 'feature-phones', isActive: true, sortOrder: 3 },
    ]
  },
  {
    id: '4',
    name: 'Accessories',
    slug: 'accessories',
    description: 'Cables, cases, and peripherals',
    image: 'https://images.pexels.com/photos/2115256/pexels-photo-2115256.jpeg?auto=compress&cs=tinysrgb&w=400',
    isActive: true,
    sortOrder: 4,
    subcategories: [
      { id: '4-1', name: 'Keyboards & Mice', slug: 'keyboards-mice', isActive: true, sortOrder: 1 },
      { id: '4-2', name: 'Monitors', slug: 'monitors', isActive: true, sortOrder: 2 },
      { id: '4-3', name: 'Cables & Adapters', slug: 'cables-adapters', isActive: true, sortOrder: 3 },
      { id: '4-4', name: 'Cases & Covers', slug: 'cases-covers', isActive: true, sortOrder: 4 },
      { id: '4-5', name: 'Audio', slug: 'audio', isActive: true, sortOrder: 5 },
    ]
  }
];

export const mockProducts: Product[] = [
  {
    id: '1',
    name: 'MacBook Pro 16" M3 Max',
    description: 'The most powerful MacBook Pro ever is here. With the blazing-fast M3 Max chip — the most advanced chip ever built for a personal computer — MacBook Pro delivers exceptional performance whether you\'re editing massive photography projects, coding the next breakthrough app, or creating your next masterpiece.',
    shortDescription: 'Powerful laptop with M3 Max chip for professional work',
    category: 'laptops',
    subcategory: 'business-laptops',
    brand: 'Apple',
    model: 'MacBook Pro 16" 2024',
    price: 299999,
    originalPrice: 349999,
    costPrice: 250000,
    stock: 15,
    minStock: 5,
    sku: 'MBP-16-M3-MAX-001',
    barcode: '194253715849',
    weight: 2.16,
    dimensions: { length: 35.57, width: 24.81, height: 1.68 },
    images: [
      'https://images.pexels.com/photos/18105/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=500',
      'https://images.pexels.com/photos/18105/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=500'
    ],
    specifications: [
      { name: 'Processor', value: 'Apple M3 Max chip', group: 'Performance' },
      { name: 'Memory', value: '32GB unified memory', group: 'Performance' },
      { name: 'Storage', value: '1TB SSD', group: 'Storage' },
      { name: 'Display', value: '16.2-inch Liquid Retina XDR display', group: 'Display' },
      { name: 'Graphics', value: '40-core GPU', group: 'Performance' },
      { name: 'Battery', value: 'Up to 22 hours', group: 'Power' },
      { name: 'Ports', value: '3x Thunderbolt 4, HDMI, SDXC, MagSafe 3', group: 'Connectivity' },
      { name: 'Operating System', value: 'macOS Sonoma', group: 'Software' }
    ],
    features: [
      'M3 Max chip with 16-core CPU',
      '40-core GPU for graphics-intensive tasks',
      '32GB unified memory',
      '1TB SSD storage',
      '16.2-inch Liquid Retina XDR display',
      'Up to 22 hours battery life',
      'Advanced camera and audio',
      'Magic Keyboard with Touch ID'
    ],
    tags: [
      { id: 'featured', name: 'Featured', type: 'featured', color: '#3B82F6' },
      { id: 'top_sales', name: 'Best Seller', type: 'top_sales', color: '#10B981' }
    ],
    status: 'active',
    visibility: 'public',
    seoTitle: 'MacBook Pro 16" M3 Max - Professional Laptop | FastHub Computers',
    seoDescription: 'Get the powerful MacBook Pro 16" with M3 Max chip. Perfect for professionals, creators, and developers. Free delivery in Kenya.',
    seoKeywords: ['MacBook Pro', 'M3 Max', 'Apple laptop', 'professional laptop', 'Kenya'],
    rating: 4.9,
    reviewCount: 128,
    totalSales: 89,
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-15T10:30:00Z',
    createdBy: 'admin',
    updatedBy: 'admin'
  },
  {
    id: '2',
    name: 'iPhone 15 Pro Max',
    description: 'iPhone 15 Pro Max. Forged in titanium and featuring the groundbreaking A17 Pro chip, a customizable Action Button, and the most powerful iPhone camera system ever.',
    shortDescription: 'Latest iPhone with advanced camera system and titanium design',
    category: 'phones',
    subcategory: 'smartphones',
    brand: 'Apple',
    model: 'iPhone 15 Pro Max',
    price: 179999,
    originalPrice: 199999,
    costPrice: 150000,
    stock: 25,
    minStock: 10,
    sku: 'IPH-15-PM-256-001',
    barcode: '194253715856',
    weight: 0.221,
    dimensions: { length: 15.99, width: 7.69, height: 0.83 },
    images: [
      'https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg?auto=compress&cs=tinysrgb&w=500'
    ],
    specifications: [
      { name: 'Processor', value: 'A17 Pro chip', group: 'Performance' },
      { name: 'Storage', value: '256GB', group: 'Storage' },
      { name: 'Display', value: '6.7-inch Super Retina XDR', group: 'Display' },
      { name: 'Camera', value: '48MP Main + 12MP Ultra Wide + 12MP Telephoto', group: 'Camera' },
      { name: 'Battery', value: 'Up to 29 hours video playback', group: 'Power' },
      { name: 'Material', value: 'Titanium', group: 'Design' },
      { name: 'Operating System', value: 'iOS 17', group: 'Software' }
    ],
    features: [
      'A17 Pro chip with 6-core GPU',
      'Titanium design',
      'Action Button',
      '48MP camera system',
      'USB-C connectivity',
      'Face ID',
      'MagSafe wireless charging'
    ],
    tags: [
      { id: 'featured', name: 'Featured', type: 'featured', color: '#3B82F6' },
      { id: 'new', name: 'New', type: 'new', color: '#8B5CF6' }
    ],
    status: 'active',
    visibility: 'public',
    rating: 4.8,
    reviewCount: 256,
    totalSales: 156,
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-15T10:30:00Z',
    createdBy: 'admin',
    updatedBy: 'admin'
  }
];

export const mockRepairRequests: RepairRequest[] = [
  {
    id: 'REP-001',
    customerName: 'John Doe',
    customerEmail: 'john@example.com',
    customerPhone: '+254 700 123 456',
    deviceType: 'Laptop',
    deviceBrand: 'Dell',
    deviceModel: 'XPS 13',
    issueDescription: 'Screen is cracked and laptop won\'t turn on. Happened after dropping it.',
    urgency: 'high',
    estimatedCost: 15000,
    status: 'diagnosed',
    submittedAt: '2024-01-15T09:00:00Z',
    updatedAt: '2024-01-15T14:30:00Z',
    notes: 'Customer needs laptop for work urgently',
    technicianNotes: 'Screen replacement needed, also checking motherboard for damage'
  },
  {
    id: 'REP-002',
    customerName: 'Jane Smith',
    customerEmail: 'jane@example.com',
    customerPhone: '+254 701 234 567',
    deviceType: 'Phone',
    deviceBrand: 'Samsung',
    deviceModel: 'Galaxy S23',
    issueDescription: 'Phone keeps restarting randomly and battery drains very fast.',
    urgency: 'medium',
    status: 'in_progress',
    submittedAt: '2024-01-14T11:30:00Z',
    updatedAt: '2024-01-15T10:00:00Z',
    technicianNotes: 'Running diagnostics, likely software issue'
  }
];