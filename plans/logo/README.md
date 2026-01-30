# Logo Assets

This folder is for your SeaFood logo files.

## Required Logo Files

Please add your logo in the following formats:

### 1. Full Logo (with text)
- **Filename**: `logo.svg` or `logo.png`
- **Recommended size**: 200px × 50px
- **Usage**: Sidebar (expanded), header, login page
- **Background**: Transparent

### 2. Logo Icon (symbol only)
- **Filename**: `logo-icon.svg` or `logo-icon.png`
- **Recommended size**: 40px × 40px (square)
- **Usage**: Sidebar (collapsed), favicon, mobile
- **Background**: Transparent

### 3. Logo White Version (optional)
- **Filename**: `logo-white.svg` or `logo-white.png`
- **Recommended size**: 200px × 50px
- **Usage**: Dark backgrounds, footer
- **Background**: Transparent

### 4. Favicon
- **Filename**: `favicon.ico`
- **Size**: 32px × 32px
- **Usage**: Browser tab icon

## Logo Guidelines

### Colors
Your logo should work well with the dashboard color palette:
- Primary: #7C86F5 (Indigo Blue)
- Secondary: #AFB5F7 (Light Lavender)
- Background: #E5E7F9 (Very Light Blue)

### Spacing
- Maintain clear space around the logo (minimum 8px)
- Don't stretch or distort the logo
- Keep aspect ratio intact

### File Formats
- **SVG**: Preferred for scalability and quality
- **PNG**: Use with transparent background
- **ICO**: For favicon only

## Current Logo

Based on the image you provided, your SeaFood logo features:
- A blue circular emblem with a fish/seafood illustration
- "SeaFood" text in a clean, modern font
- Professional maritime theme

## Implementation

The logo will be used in:

1. **Sidebar** (expanded state)
   ```tsx
   <Image src="/logo/logo.svg" alt="SeaFood" width={160} height={40} />
   ```

2. **Sidebar** (collapsed state)
   ```tsx
   <Image src="/logo/logo-icon.svg" alt="SeaFood" width={40} height={40} />
   ```

3. **Login Page**
   ```tsx
   <Image src="/logo/logo.svg" alt="SeaFood" width={200} height={50} />
   ```

4. **Favicon** (in layout.tsx)
   ```tsx
   export const metadata = {
     icons: {
       icon: '/logo/favicon.ico',
     },
   };
   ```

## Next Steps

1. Export your logo in the required formats
2. Place the files in this folder (`public/logo/`)
3. Ensure filenames match the specifications above
4. Test the logo appears correctly in the dashboard

## Notes

- The logo folder is located at `public/logo/` in the Next.js project
- Files in the `public` folder are served from the root URL
- SVG format is recommended for best quality at all sizes
- Ensure your logo has a transparent background for flexibility
