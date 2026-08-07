import { useEffect, useState } from "react";
import { api } from "../api";
import {
  Empty,
  ErrorMessage,
  Loading,
  PageHeader,
  SuccessMessage,
} from "../components/Ui";

const initialApartment = {
  property_id: "",
  apartment_number: "",
  floor: "",
  contact_name: "",
  contact_phone: "",
  contact_email: "",
};

const initialProperty = {
  name: "",
  address: "",
  postal_code: "",
  city: "",
};

export default function Apartments() {
  const [items, setItems] = useState(null);
  const [properties, setProperties] = useState([]);
  const [apartmentForm, setApartmentForm] = useState(initialApartment);
  const [propertyForm, setPropertyForm] = useState(initialProperty);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState("");
  const [savingApartment, setSavingApartment] = useState(false);
  const [savingProperty, setSavingProperty] = useState(false);

  async function load() {
    try {
      const [apartments, propertyItems] = await Promise.all([
        api.apartments(),
        api.properties(),
      ]);
      setItems(apartments);
      setProperties(propertyItems);
      setError(null);
    } catch (err) {
      setError(err);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function submitProperty(event) {
    event.preventDefault();
    setSavingProperty(true);
    setError(null);
    setSuccess("");

    try {
      const createdProperty = await api.createProperty({
        ...propertyForm,
        postal_code: propertyForm.postal_code || null,
      });

      setPropertyForm(initialProperty);
      setApartmentForm((current) => ({
        ...current,
        property_id: String(createdProperty.id),
      }));
      setSuccess(
        `Immobilie „${createdProperty.name}“ wurde erstellt und für die neue Wohnung ausgewählt.`,
      );
      await load();
    } catch (err) {
      setError(err);
    } finally {
      setSavingProperty(false);
    }
  }

  async function submitApartment(event) {
    event.preventDefault();
    setSavingApartment(true);
    setError(null);
    setSuccess("");

    try {
      await api.createApartment({
        ...apartmentForm,
        property_id: Number(apartmentForm.property_id),
        floor: apartmentForm.floor || null,
        contact_name: apartmentForm.contact_name || null,
        contact_phone: apartmentForm.contact_phone || null,
        contact_email: apartmentForm.contact_email || null,
      });

      setApartmentForm(initialApartment);
      setSuccess("Wohnung wurde erfolgreich hinzugefügt.");
      await load();
    } catch (err) {
      setError(err);
    } finally {
      setSavingApartment(false);
    }
  }

  if (!items && !error) return <Loading />;

  return (
    <>
      <PageHeader
        title="Wohnungen"
        subtitle="Immobilien, Wohnungen und Kontaktpersonen verwalten."
      />

      {error && <ErrorMessage error={error} />}
      {success && <SuccessMessage>{success}</SuccessMessage>}

      <div className="split-grid">
        <section className="panel">
          <h2>Wohnungen</h2>
          {(items || []).length === 0 ? (
            <Empty>
              Noch keine Wohnungen vorhanden. Erstelle zuerst rechts eine
              Immobilie und anschließend eine Wohnung.
            </Empty>
          ) : (
            <div className="card-list">
              {(items || []).map((apartment) => (
                <article key={apartment.id}>
                  <strong>
                    {apartment.property_name} · Whg. {apartment.apartment_number}
                  </strong>
                  <span>{apartment.property_address}</span>
                  <small>
                    {apartment.contact_name || "Keine Kontaktperson"}
                    {apartment.contact_phone
                      ? ` · ${apartment.contact_phone}`
                      : ""}
                  </small>
                </article>
              ))}
            </div>
          )}
        </section>

        <div>
          <section className="panel">
            <h2>Immobilie hinzufügen</h2>
            <form className="stack-form" onSubmit={submitProperty}>
              <label>
                Bezeichnung
                <input
                  required
                  minLength="2"
                  placeholder="z. B. Wohnhaus Sonnenstraße"
                  value={propertyForm.name}
                  onChange={(event) =>
                    setPropertyForm({
                      ...propertyForm,
                      name: event.target.value,
                    })
                  }
                />
              </label>

              <label>
                Adresse
                <input
                  required
                  minLength="3"
                  placeholder="Sonnenstraße 12"
                  value={propertyForm.address}
                  onChange={(event) =>
                    setPropertyForm({
                      ...propertyForm,
                      address: event.target.value,
                    })
                  }
                />
              </label>

              <label>
                Postleitzahl
                <input
                  placeholder="80331"
                  value={propertyForm.postal_code}
                  onChange={(event) =>
                    setPropertyForm({
                      ...propertyForm,
                      postal_code: event.target.value,
                    })
                  }
                />
              </label>

              <label>
                Ort
                <input
                  required
                  minLength="2"
                  placeholder="München"
                  value={propertyForm.city}
                  onChange={(event) =>
                    setPropertyForm({
                      ...propertyForm,
                      city: event.target.value,
                    })
                  }
                />
              </label>

              <button
                className="button primary"
                type="submit"
                disabled={savingProperty}
              >
                {savingProperty ? "Wird gespeichert …" : "Immobilie speichern"}
              </button>
            </form>
          </section>

          <section className="panel">
            <h2>Wohnung hinzufügen</h2>

            {properties.length === 0 && (
              <div className="alert error">
                Zuerst muss eine Immobilie angelegt werden.
              </div>
            )}

            <form className="stack-form" onSubmit={submitApartment}>
              <label>
                Immobilie
                <select
                  required
                  disabled={properties.length === 0}
                  value={apartmentForm.property_id}
                  onChange={(event) =>
                    setApartmentForm({
                      ...apartmentForm,
                      property_id: event.target.value,
                    })
                  }
                >
                  <option value="">Bitte wählen</option>
                  {properties.map((property) => (
                    <option key={property.id} value={property.id}>
                      {property.name} · {property.address}
                    </option>
                  ))}
                </select>
              </label>

              <label>
                Wohnungsnummer
                <input
                  required
                  value={apartmentForm.apartment_number}
                  onChange={(event) =>
                    setApartmentForm({
                      ...apartmentForm,
                      apartment_number: event.target.value,
                    })
                  }
                />
              </label>

              <label>
                Etage
                <input
                  value={apartmentForm.floor}
                  onChange={(event) =>
                    setApartmentForm({
                      ...apartmentForm,
                      floor: event.target.value,
                    })
                  }
                />
              </label>

              <label>
                Kontaktperson
                <input
                  value={apartmentForm.contact_name}
                  onChange={(event) =>
                    setApartmentForm({
                      ...apartmentForm,
                      contact_name: event.target.value,
                    })
                  }
                />
              </label>

              <label>
                Telefon
                <input
                  value={apartmentForm.contact_phone}
                  onChange={(event) =>
                    setApartmentForm({
                      ...apartmentForm,
                      contact_phone: event.target.value,
                    })
                  }
                />
              </label>

              <label>
                E-Mail
                <input
                  type="email"
                  value={apartmentForm.contact_email}
                  onChange={(event) =>
                    setApartmentForm({
                      ...apartmentForm,
                      contact_email: event.target.value,
                    })
                  }
                />
              </label>

              <button
                className="button primary"
                type="submit"
                disabled={properties.length === 0 || savingApartment}
              >
                {savingApartment ? "Wird gespeichert …" : "Wohnung speichern"}
              </button>
            </form>
          </section>
        </div>
      </div>
    </>
  );
}
