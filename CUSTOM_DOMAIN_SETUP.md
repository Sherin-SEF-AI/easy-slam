# Custom Domain Setup Guide for EasySLAM

This guide will help you set up the custom domain `easyslam.ai` for your EasySLAM GitHub Pages site.

## 🌐 Domain: easyslam.ai

### Step 1: Purchase the Domain

1. **Choose a Domain Registrar** (recommended options):
   - **Namecheap** (affordable, good support)
   - **Google Domains** (reliable, good integration)
   - **GoDaddy** (popular, extensive features)
   - **Cloudflare** (free DNS, good security)

2. **Purchase easyslam.ai**:
   - Search for `easyslam.ai` availability
   - Purchase the domain (typically $10-15/year)
   - Complete the registration process

### Step 2: Configure DNS Records

Once you have the domain, configure these DNS records:

#### A Records (for root domain):
```
Type: A
Name: @
Value: 185.199.108.153
TTL: 3600

Type: A
Name: @
Value: 185.199.109.153
TTL: 3600

Type: A
Name: @
Value: 185.199.110.153
TTL: 3600

Type: A
Name: @
Value: 185.199.111.153
TTL: 3600
```

#### CNAME Record (for www subdomain):
```
Type: CNAME
Name: www
Value: sherin-sef-ai.github.io
TTL: 3600
```

### Step 3: GitHub Pages Configuration

1. **Go to your repository**: https://github.com/Sherin-SEF-AI/easy-slam

2. **Navigate to Settings**:
   - Click "Settings" tab
   - Scroll down to "Pages" in the left sidebar

3. **Configure Custom Domain**:
   - In the "Custom domain" field, enter: `easyslam.ai`
   - Check "Enforce HTTPS" (recommended)
   - Click "Save"

4. **Verify Configuration**:
   - GitHub will create a CNAME file in your repository
   - The file should contain: `easyslam.ai`

### Step 4: SSL Certificate

GitHub Pages automatically provides SSL certificates for custom domains:

1. **Wait for SSL**: It may take up to 24 hours for the SSL certificate to be issued
2. **Check Status**: You can verify SSL status at https://www.ssllabs.com/ssltest/
3. **Force HTTPS**: Ensure "Enforce HTTPS" is checked in GitHub Pages settings

### Step 5: Test Your Domain

After DNS propagation (can take up to 48 hours):

1. **Test the main domain**: https://easyslam.ai
2. **Test www subdomain**: https://www.easyslam.ai
3. **Test HTTPS**: Ensure both work with SSL

### Step 6: Update Documentation

The following files have been updated to reference your custom domain:

- ✅ `docs/index.html` - Landing page with easyslam.ai links
- ✅ `CNAME` - GitHub Pages custom domain configuration
- ✅ `README.md` - Updated with custom domain references

### DNS Propagation Check

You can check DNS propagation using these tools:
- https://www.whatsmydns.net/
- https://dnschecker.org/
- https://www.dnsstuff.com/

### Troubleshooting

#### Common Issues:

1. **Domain not resolving**:
   - Check DNS records are correct
   - Wait for DNS propagation (up to 48 hours)
   - Verify domain registrar settings

2. **SSL certificate issues**:
   - Ensure "Enforce HTTPS" is enabled in GitHub Pages
   - Wait up to 24 hours for certificate issuance
   - Check for mixed content warnings

3. **CNAME conflicts**:
   - Ensure no conflicting CNAME records exist
   - Check for redirects or forwarding settings

#### Verification Commands:

```bash
# Check DNS resolution
nslookup easyslam.ai
dig easyslam.ai

# Check SSL certificate
openssl s_client -connect easyslam.ai:443 -servername easyslam.ai
```

### Alternative Domain Options

If `easyslam.ai` is not available, consider these alternatives:

- `easyslam.dev`
- `easyslam.tech`
- `easyslam.io`
- `easyslam.com`
- `easyslam.org`

### Cost Breakdown

**Annual Costs**:
- Domain registration: $10-15/year
- DNS hosting: Usually free with registrar
- SSL certificate: Free (provided by GitHub Pages)
- **Total**: ~$10-15/year

### Security Considerations

1. **Enable HTTPS**: Always enforce HTTPS in GitHub Pages
2. **DNS Security**: Consider using Cloudflare for additional security
3. **Domain Lock**: Enable domain lock at your registrar
4. **WHOIS Privacy**: Enable WHOIS privacy protection

### Monitoring

Set up monitoring for your domain:

1. **Uptime Monitoring**: Use services like UptimeRobot or Pingdom
2. **SSL Monitoring**: Monitor SSL certificate expiration
3. **DNS Monitoring**: Check DNS resolution regularly

### Final Checklist

- [ ] Domain purchased (easyslam.ai)
- [ ] DNS records configured
- [ ] GitHub Pages custom domain set
- [ ] SSL certificate issued
- [ ] Domain resolves correctly
- [ ] HTTPS working
- [ ] Documentation updated
- [ ] Monitoring configured

### Support

If you encounter issues:

1. **GitHub Support**: https://docs.github.com/en/pages
2. **Domain Registrar Support**: Contact your registrar's support
3. **Community**: GitHub Discussions in your repository

---

**Note**: This setup will make your EasySLAM documentation available at `https://easyslam.ai` with professional branding and SSL security. 