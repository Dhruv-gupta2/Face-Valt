# FaceVault Usage Guide

Complete guide to using FaceVault for face registration and recognition.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Registering Faces](#registering-faces)
3. [Recognizing Faces](#recognizing-faces)
4. [Managing Faces](#managing-faces)
5. [Best Practices](#best-practices)
6. [Common Use Cases](#common-use-cases)
7. [Tips & Tricks](#tips--tricks)

## Getting Started

### Starting the System

**Quick Start:**
```bash
./start.sh  # Linux/Mac
start.bat   # Windows
```

**Manual Start:**
1. Start backend: `cd backend && python app.py`
2. Open frontend: `frontend/index.html` in browser

### Interface Overview

The FaceVault interface has three main sections:

1. **📸 Register Face** - Add new faces to the system
2. **🔍 Recognize Face** - Identify people in photos
3. **👥 Registered Faces** - View and manage all faces

## Registering Faces

### Step-by-Step Registration

1. **Enter Name**
   - Type the person's full name
   - Use consistent naming (e.g., "John Smith" not "john" or "JOHN")
   - Names are case-sensitive

2. **Upload Photo**
   - Click the upload zone
   - Select a clear photo of the person
   - Wait for preview to appear

3. **Register**
   - Click "Register Face" button
   - Wait for confirmation message
   - Face is now saved permanently

### Photo Requirements for Registration

✅ **Good Photos:**
- Front-facing, looking at camera
- Well-lit (natural or bright indoor light)
- Clear, in-focus image
- Entire face visible (no sunglasses or masks)
- Neutral expression
- Resolution: 640x480 or higher
- Only ONE face in the image

❌ **Avoid:**
- Side profiles or angled faces
- Dark or backlit photos
- Blurry or low-resolution images
- Multiple people in frame
- Sunglasses, masks, or face coverings
- Extreme expressions
- Heavy filters or edits

### Registration Tips

**For Best Results:**

1. **Lighting**: Use even, front-facing lighting
2. **Background**: Plain, uncluttered background
3. **Distance**: Face should fill 40-60% of frame
4. **Quality**: Use original photos, not screenshots
5. **Multiple Photos**: Register the same person 2-3 times with slight variations for better accuracy

**Example Workflow:**
```
Person: Alice Johnson
Photo 1: Front-facing, neutral
Photo 2: Front-facing, smiling
Photo 3: Front-facing, slight angle
```

## Recognizing Faces

### Step-by-Step Recognition

1. **Upload Photo**
   - Click upload zone in "Recognize Face" section
   - Select photo containing one or more faces
   - Wait for preview

2. **Run Recognition**
   - Click "Recognize" button
   - System will analyze all faces in image
   - Results appear with confidence scores

3. **Review Results**
   - Green boxes highlight detected faces
   - Names displayed with confidence percentage
   - "Unknown" appears for unregistered faces

### Understanding Results

**Confidence Scores:**
- **95-100%**: Excellent match, very confident
- **85-94%**: Good match, confident
- **75-84%**: Acceptable match, fairly confident
- **60-74%**: Weak match, less confident
- **Below 60%**: Not recognized (shows as "Unknown")

**Face Detection Boxes:**
- Green box with name = Successfully recognized
- Box position shows exact location of face
- Multiple boxes for multiple faces

### Recognition Tips

**For Accurate Recognition:**

1. **Image Quality**: Use clear, well-lit photos
2. **Face Size**: Faces should be visible and not too small
3. **Face Angle**: Front or slight angle works best
4. **Consistency**: Recognition works best with similar lighting to registration photo
5. **Updates**: Re-register people if appearance changes significantly

**Troubleshooting Recognition:**

| Issue | Solution |
|-------|----------|
| "No face detected" | Ensure face is clearly visible and front-facing |
| Low confidence score | Re-register with better quality photo |
| Wrong person identified | Check if two people look similar; adjust tolerance |
| "Unknown" for registered person | Try different photo or re-register |

## Managing Faces

### Viewing Registered Faces

- Scroll to "Registered Faces" section
- See all registered people with dates
- Total count displayed at top

### Deleting Faces

1. Find person in "Registered Faces" list
2. Click "Delete" button
3. Confirm deletion
4. Face and all associated data removed permanently

**When to Delete:**
- Person no longer needs to be in system
- Incorrect registration
- Want to re-register with better photo
- Testing or development purposes

### Database Management

**Storage Location:**
- Database: `database/faces.db`
- Images: `database/images/`
- Face encodings: Stored as binary in database

**Backup:**
```bash
# Backup database
cp database/faces.db database/faces_backup_$(date +%Y%m%d).db

# Backup images
cp -r database/images database/images_backup_$(date +%Y%m%d)
```

**Restore:**
```bash
# Restore database
cp database/faces_backup_YYYYMMDD.db database/faces.db

# Restore images
cp -r database/images_backup_YYYYMMDD database/images
```

## Best Practices

### Registration Best Practices

1. **Consistent Naming Convention**
   ```
   Good: "John Smith", "Jane Doe"
   Avoid: "john", "SMITH", "J. Smith"
   ```

2. **Quality Control**
   - Review each photo before registration
   - Ensure clear, front-facing shots
   - Verify only one face per registration

3. **Multiple Registrations** (Optional)
   - Register same person 2-3 times
   - Use photos from different occasions
   - Helps with varying lighting/angles

4. **Regular Updates**
   - Update photos if appearance changes
   - Re-register after significant changes (beard, glasses, etc.)
   - Archive old registrations

### Recognition Best Practices

1. **Test Environment**
   - Test with known faces first
   - Verify accuracy before production use
   - Adjust tolerance if needed

2. **Image Preparation**
   - Resize large images before upload
   - Crop to relevant area if possible
   - Ensure adequate lighting

3. **Batch Processing**
   - For multiple faces, use group photos
   - System handles multiple faces simultaneously
   - Review each result individually

### Security Best Practices

1. **Access Control**
   - Limit who can register faces
   - Track registrations with timestamps
   - Regular audit of registered faces

2. **Data Privacy**
   - Inform people before registering
   - Follow local privacy regulations
   - Provide opt-out mechanism

3. **Backup Regularly**
   - Weekly database backups
   - Store backups securely
   - Test restore procedures

## Common Use Cases

### 1. Employee Badge System

**Setup:**
1. Register all employees with ID photos
2. Use consistent photo style
3. Update quarterly or as needed

**Usage:**
- Take photo at entrance
- System identifies employee
- Grant access based on recognition

### 2. Photo Organization

**Setup:**
1. Register family members or friends
2. Use multiple photos per person
3. Include nicknames if desired

**Usage:**
- Upload family photos
- System identifies everyone
- Tag and organize automatically

### 3. Event Check-In

**Setup:**
1. Pre-register attendees
2. Use registration photos
3. Set up check-in station

**Usage:**
- Quick photo at entrance
- Instant identification
- Fast, contactless check-in

### 4. Security Monitoring

**Setup:**
1. Register authorized personnel
2. Use high-quality photos
3. Maintain updated database

**Usage:**
- Monitor access points
- Alert on unknown faces
- Log all recognitions

## Tips & Tricks

### Performance Tips

**Faster Recognition:**
```python
# In backend/app.py, adjust these:
- Use smaller images (800-1200px)
- Reduce face detection resolution
- Use HOG model (not CNN)
```

**Better Accuracy:**
```python
# Adjust tolerance (lower = stricter):
tolerance=0.5  # More accurate, may miss some
tolerance=0.6  # Default, balanced
tolerance=0.7  # More lenient, may have false positives
```

### Workflow Optimization

**Bulk Registration:**
1. Prepare all photos in advance
2. Use consistent file naming
3. Register in batches
4. Verify each registration

**Quick Recognition:**
1. Keep registration photos updated
2. Use consistent lighting
3. Pre-crop images to face area
4. Test with sample images first

### Advanced Usage

**API Integration:**
```javascript
// Register face programmatically
fetch('http://localhost:5000/api/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'John Doe',
    image: base64ImageData
  })
});

// Recognize faces
fetch('http://localhost:5000/api/recognize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    image: base64ImageData
  })
});
```

**Custom Frontend:**
- Use the API endpoints
- Build mobile app
- Integrate with existing system
- Add custom features

### Troubleshooting Workflow

**If Recognition Fails:**

1. ✓ Check if face is registered
2. ✓ Verify photo quality
3. ✓ Try different lighting
4. ✓ Re-register with better photo
5. ✓ Adjust tolerance setting
6. ✓ Check backend logs

**If Registration Fails:**

1. ✓ Verify only one face in image
2. ✓ Check image format (JPG, PNG)
3. ✓ Ensure face is clearly visible
4. ✓ Try different photo
5. ✓ Check backend is running
6. ✓ Review error messages

## Keyboard Shortcuts

While using the interface:

- `Tab` - Navigate between fields
- `Enter` - Submit form (when focused)
- `Esc` - Clear current selection
- `Ctrl+R` - Refresh page
- `F12` - Open browser dev tools (for debugging)

## Getting Help

### Resources

1. **Documentation**
   - README.md - Overview
   - INSTALLATION.md - Setup guide
   - This file - Usage guide

2. **Logs**
   - Browser console (F12)
   - Backend logs: `backend/facevault.log`

3. **Testing**
   - Run `python test.py` to check system
   - Test with known photos first
   - Verify each feature works

### Support

If issues persist:
1. Check logs for errors
2. Review this guide
3. Try with different photos
4. Restart the system
5. Report issue with details

---

**Happy face recognizing!** 🎉

For technical details, see the [API Documentation](README.md#api-endpoints).
