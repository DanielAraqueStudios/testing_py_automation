from string import Template
import os

def select_services():
    print("\n=== Selección de Servicios ===")
    print("Seleccione los servicios a incluir en la cotización:")
    services = {
        'web': input("¿Incluir desarrollo web? (s/n): ").lower() == 's',
        'social': input("¿Incluir redes sociales? (s/n): ").lower() == 's',
        'bot': input("¿Incluir bot de WhatsApp? (s/n): ").lower() == 's',
        'facebook': input("¿Incluir campañas de Facebook? (s/n): ").lower() == 's',
        'ai': input("¿Incluir capacitación en IA? (s/n): ").lower() == 's'
    }
    return services

def get_user_input():
    print("=== Sistema de Generación de Cotizaciones ===")
    
    # Client Information
    client_names = input("Ingrese los nombres de los clientes (separados por coma): ")
    client_position = input("Ingrese el cargo del cliente: ")
    
    # Company Information
    company_name = input("Ingrese el nombre de la empresa: ")
    sender_name = input("Ingrese el nombre del remitente: ")
    sender_position = input("Ingrese el cargo del remitente: ")
    
    # Select services
    services = select_services()
    
    # Only ask for prices of selected services
    prices = {}
    if services['web']:
        prices['web_original'] = float(input("Precio original desarrollo web: "))
        prices['web_discounted'] = float(input("Precio con descuento desarrollo web: "))
    
    if services['social']:
        prices['social_original'] = float(input("Precio original redes sociales: "))
        prices['social_discounted'] = float(input("Precio con descuento redes sociales: "))
    
    if services['bot']:
        prices['bot_original'] = float(input("Precio original bot WhatsApp: "))
        prices['bot_discounted'] = float(input("Precio con descuento bot WhatsApp: "))
    
    if services['facebook']:
        prices['facebook_original'] = float(input("Precio original campañas Facebook: "))
        prices['facebook_discounted'] = float(input("Precio con descuento campañas Facebook: "))
    
    if services['ai']:
        prices['ai_original'] = float(input("Precio original capacitación IA: "))
        prices['ai_discounted'] = float(input("Precio con descuento capacitación IA: "))

    # Offer Terms
    validity_days = input("Días de validez de la oferta: ")
    payment_terms = input("Términos de pago: ")
    
    variables = {
        'client_names': client_names,
        'client_position': client_position,
        'company_name': company_name,
        'sender_name': sender_name,
        'sender_position': sender_position,
        'validity_days': validity_days,
        'payment_terms': payment_terms,
        # Add service text variables
        'web_service': 'Desarrollo web, ' if services['web'] else '',
        'bot_service': 'bot de whatsapp, ' if services['bot'] else '',
        'facebook_service': 'campañas de tráfico pago, ' if services['facebook'] else '',
        'social_service': 'estrategia en redes sociales' if services['social'] else '',
        'ai_service': ' y capacitación en inteligencia artificial' if services['ai'] else '',
        # Add service flags
        'show_web': 'true' if services['web'] else 'false',
        'show_social': 'true' if services['social'] else 'false',
        'show_bot': 'true' if services['bot'] else 'false',
        'show_facebook': 'true' if services['facebook'] else 'false',
        'show_ai': 'true' if services['ai'] else 'false',
        # Add section content
        'web_section': '''
            <section class="section" id="testimonials">
        <div class="container">
          <div class="row">
            <div class="col-lg-8 offset-lg-2">
              <div class="center-heading">
                <h2>PÁGINA <em>
                  WEB
                </em>
                <p>Características de la página
                </p>
              </h2>

              </div>
            </div>
          </div>
        </div>
      </section>


     
      <section class="section" id="about">
        <div class="container">
            <div class="row">
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter left move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>01</h2>
                            <img src="assets/images/features-icon-1.png" alt="">
                            <h4>A medida</h4>
                            <p>Desarrollo completamente a medida, con subpáginas, menús desplegables, botón de WhatsApp y de redes sociales. Tanto los botones, colores, tipografía y en general toda la página.</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter bottom move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>02</h2>
                            <img src="assets/images/features-icon-2.png" alt="">
                            <h4>Tecnologías</h4>
                            <p>Desarrollo de eccomerce con carrito de compras , diseño responsive que se adapta a diferentes dispositivos (iPad, tablets, computadores, televisores y dispositivos móviles).</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>03</h2>
                            <img src="assets/images/features-icon-3.png" alt="">
                            <h4>Posicionamiento SEO</h4>
                            <p>Posicionamiento orgánico, tu página aparece de primera en Google  en los primeros lugares de búsqueda al colocar el nombre de la empresa.</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>04</h2>
                            <img src="assets/images/features-icon-3.png" alt="">
                            <h4>UI/UX + mapas de calor</h4>
                            <p>Tú página tendrá una tecnología basada en mapas de calor, donde por medio del diseño minimalista se predice estadísticamente los lugares en que se posicionará el mouse para colocar los botones y llamadas a la acción en dichos lugares.</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>05</h2>
                            <img src="assets/images/features-icon-3.png" alt="">
                            <h4>Carrito de compras</h4>
                            <p>Permite agregar productos al carrito de compras y procesar los pagos online ,pagar con difeentes medios de pago.</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                    data-scroll-reveal="enter right move 30px over 0.6s after 0.4s">
                    <div class="features-item">
                        <div class="features-icon">
                            <h2>06</h2>
                            <img src="assets/images/features-icon-3.png" alt="">
                            <h4>Cuentas de correo</h4>
                            <p>Se incluyen hasta 10 cuentas de correo electrónico (depende del nombre del hosting). Ej: nombre del hosting: nextcompany.com, correo: gerencia@nexthosting.com.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
            ''' if services['web'] else '',
        
        'social_section': '''
            <section class="section" id="social">
                // ... social media content ...
            </section>
        ''' if services['social'] else '',
        
        'bot_section': '''
            <section class="section" id="bot">
                // ... bot content ...
            </section>
        ''' if services['bot'] else '',
        
        'facebook_section': '''
            <section class="section" id="facebook">
                // ... facebook content ...
            </section>
        ''' if services['facebook'] else '',
        
        'ai_section': '''
            <section class="section" id="ai">
                // ... ai training content ...
            </section>
        ''' if services['ai'] else ''
    }

    # Add prices only for selected services
    for service, price_data in prices.items():
        variables[service] = format_price(price_data)

    return variables

def format_price(price):
    return "{:,.0f}".format(price).replace(",", ".")

def generate_html(template_path, output_path, variables):
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            template_content = file.read()
        
        template = Template(template_content)
        filled_template = template.safe_substitute(variables)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(filled_template)
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    # Define paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, 'template.html')
    output_path = os.path.join(current_dir, 'cotizacion_generada.html')
    
    # Get user input
    variables = get_user_input()
    
    # Generate HTML
    if generate_html(template_path, output_path, variables):
        print(f"\nCotización generada exitosamente en: {output_path}")
    else:
        print("Error al generar la cotización")



if __name__ == "__main__":
    main()
