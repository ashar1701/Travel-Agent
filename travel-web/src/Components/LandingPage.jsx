import { useState } from 'react'

const defaultFormState = {
  from: '',
  to: '',
  departureDate: '',
  returnDate: ''
}

function LandingPage() {
  const [formData, setFormData] = useState(defaultFormState)

  const handleChange = (event) => {
    const { name, value } = event.target
    setFormData((previous) => ({ ...previous, [name]: value }))
  }

  const handleSubmit = (event) => {
    event.preventDefault()
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
                required
              />
            </label>
            <label className="field">
              <span className="field-label">Return</span>
              <input
                name="returnDate"
                type="date"
                value={formData.returnDate}
                onChange={handleChange}
                min={formData.departureDate}
              />
            </label>
          </div>
          <div className="actions">
            <button type="submit">Plan my trip</button>
          </div>
        </form>
      </section>
    </main>
  )
}

export default LandingPage
