import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="container" style={{ textAlign: 'center', padding: '60px 20px' }}>
      <h1 style={{ fontSize: '48px', marginBottom: '20px' }}>404</h1>
      <h2 style={{ fontSize: '24px', marginBottom: '20px' }}>Page Not Found</h2>
      <p style={{ marginBottom: '30px', color: '#666' }}>
        The page you're looking for doesn't exist.
      </p>
      <Link href="/" className="btn btn-primary">
        Go Back Home
      </Link>
    </div>
  );
}

