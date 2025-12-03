import { useState } from 'react'

const defaultFormState = {
  from: '',
  to: '',
  departureDate: '',
  returnDate: ''
}

function LandingPage() {
  const [formData, setFormData] = useState(defaultFormState)
  const today = new Date().toISOString().split('T')[0]

  const departureBeforeToday =
    formData.departureDate !== '' && formData.departureDate < today
  const returnBeforeDeparture =
    formData.departureDate !== '' &&
    formData.returnDate !== '' &&
    formData.returnDate < formData.departureDate
  const hasTemporalError = departureBeforeToday || returnBeforeDeparture

  const handleChange = (event) => {
    const { name, value } = event.target
    setFormData((previous) => ({ ...previous, [name]: value }))
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    if (hasTemporalError) {
      return
    }
    console.log('Trip request submitted', formData)
  }

  return (
    <main className="app-shell">
      <section className="hero">
        <p className="eyebrow">Personalized travel planning</p>
        <h1>Plan your next adventure</h1>
        <p className="tagline">
          Tell us where you would like to go and let our AI craft a tailored
          itinerary just for you.
        </p>
      </section>

      <section className="form-card" aria-label="Trip details">
        <form className="trip-form" onSubmit={handleSubmit}>
          <div className="form-grid">
            <label className="field">
              <span className="field-label">From</span>
              <input
                name="from"
                type="text"
                placeholder="City or airport"
                value={formData.from}
                onChange={handleChange}
                required
              />
            </label>
            <label className="field">
              <span className="field-label">To</span>
              <input
                name="to"
                type="text"
                placeholder="Destination city"
                value={formData.to}
                onChange={handleChange}
                required
              />
            </label>
            <label className="field">
              <span className="field-label">Departure</span>
              <input
                name="departureDate"
                type="date"
                value={formData.departureDate}
                onChange={handleChange}
                min={today}
                required
              />
              {departureBeforeToday && (
                <p className="field-hint error" role="alert">
                  Departure date cannot be earlier than today.
                </p>
              )}
            </label>
            <label className="field">
              <span className="field-label">Return</span>
              <input
                name="returnDate"
                type="date"
                value={formData.returnDate}
                onChange={handleChange}
                min={formData.departureDate || today}
              />
              {returnBeforeDeparture && (
                <p className="field-hint error" role="alert">
                  Return date must be on or after your departure date.
                </p>
              )}
            </label>
          </div>
          <div className="actions">
            <button type="submit" disabled={hasTemporalError}>
              Plan my trip
            </button>
            {hasTemporalError ? (
              <p className="helper-text error" role="alert">
                Please fix the highlighted dates above.
              </p>
            ) : (
              <p className="helper-text">We will never share your travel plans.</p>
            )}
          </div>
        </form>
      </section>
    </main>
  )
}

export default LandingPage
