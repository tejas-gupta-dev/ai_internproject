# build_faiss.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

docs = [

# ---------------- SERVER ERRORS ----------------
"To fix 500 error, check server logs for stack traces.",
"A 502 Bad Gateway error usually indicates an upstream service failure.",
"A 503 error may occur due to server overload or maintenance.",
"Ensure environment variables are correctly configured after deployment.",
"Check application logs for unhandled exceptions.",
"Restart the server after applying configuration changes.",
"Verify API routes are correctly mapped.",
"Memory leak issues often occur due to unclosed database connections.",
"Ensure all async operations are properly awaited.",
"Increase timeout settings for long-running processes.",

# ---------------- PERFORMANCE ----------------
"High latency may be caused by inefficient database queries.",
"Optimize indexing to improve database performance.",
"Enable query caching to reduce repeated database hits.",
"Use connection pooling for better performance.",
"Monitor CPU and memory usage in production.",
"Implement load balancing to distribute traffic.",
"Use autoscaling groups to handle traffic spikes.",
"Compress API responses to reduce network load.",
"Use CDN for static assets delivery.",
"Enable logging to track performance bottlenecks.",

# ---------------- DATABASE ----------------
"Ensure database migrations are properly applied.",
"Check database connection pool limits.",
"Use indexing on frequently queried columns.",
"Avoid N+1 query problems in ORM.",
"Backup the database before major upgrades.",
"Monitor slow queries using database profiling tools.",
"Use read replicas for scaling read-heavy workloads.",
"Validate foreign key constraints properly.",
"Ensure database credentials are secure.",
"Check transaction isolation levels if facing data inconsistency.",

# ---------------- SECURITY ----------------
"Ensure HTTPS is enabled in production.",
"Validate user input to prevent SQL injection.",
"Use proper authentication tokens for APIs.",
"Rotate API keys regularly.",
"Enable rate limiting to prevent abuse.",
"Use firewall rules to restrict unauthorized access.",
"Encrypt sensitive data at rest.",
"Use secure password hashing algorithms.",
"Monitor suspicious login attempts.",
"Enable multi-factor authentication for critical systems.",

# ---------------- PAYMENT ISSUES ----------------
"Clear cache and retry payment if transaction fails.",
"Verify payment gateway API keys.",
"Check payment webhook configuration.",
"Ensure currency settings match gateway configuration.",
"Retry failed payments with exponential backoff.",
"Verify SSL certificates for payment endpoints.",
"Check payment provider status dashboard.",
"Ensure callback URLs are accessible publicly.",
"Validate transaction IDs before processing.",
"Log payment failures for audit tracking.",

# ---------------- ENTERPRISE / BUSINESS ----------------
"Enterprise scaling requires load balancing and monitoring.",
"Cost-benefit analysis should include infrastructure cost.",
"ROI impact depends on operational efficiency gains.",
"Cloud auto-scaling reduces infrastructure overhead.",
"Implement monitoring dashboards for executives.",
"Analyze user engagement metrics for growth.",
"Use KPI tracking to measure performance improvements.",
"Optimize operational cost through automation.",
"Adopt microservices architecture for scalability.",
"Plan disaster recovery strategies for enterprise resilience.",

# ---------------- USER EXPERIENCE ----------------
"User frustration often increases due to repeated failures.",
"Provide clear error messages to improve user trust.",
"Ensure UI responsiveness across devices.",
"Reduce page load time for better engagement.",
"Implement proper retry mechanisms for failed actions.",
"Provide real-time feedback during operations.",
"Offer fallback mechanisms for service downtime.",
"Improve onboarding flow for better retention.",
"Use analytics to track drop-off points.",
"Ensure accessibility compliance standards are met."

]

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(docs)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

faiss.write_index(index, "kb_index.faiss")

with open("kb_docs.pkl", "wb") as f:
    pickle.dump(docs, f)
