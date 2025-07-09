export interface Alert {
  id: string
  timestamp: Date
  anomaly_type: string
  confidence: number
  description: string
  severity: "low" | "medium" | "high"
  zone: string
  camera: string
  location: {
    lat: number
    lng: number
  }
  snapshot_url?: string
  resolved: boolean
  resolvedAt?: Date
}
