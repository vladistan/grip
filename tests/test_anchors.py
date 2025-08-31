"""
Tests for anchor link functionality and case sensitivity handling.
"""

import unittest

from grip import Grip
from grip.readers import TextReader


class TestAnchorLinks(unittest.TestCase):
    """Tests for anchor link handling in grip templates."""

    def test_template_includes_case_insensitive_scroll_function(self):
        """Test that template includes the improved scrollToHash function."""
        markdown_content = '''# Test
        
## Item Section

Some content here.

## Another Section

More content.
        '''
        
        app = Grip(TextReader(markdown_content, 'test.md'), case_insensitive_anchors=True)
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Should include the enhanced scrollToHash function with case-insensitive logic
            self.assertIn('function scrollToHash', html)
            self.assertIn('hashTarget.toLowerCase()', html)
            self.assertIn('case-insensitive search', html)
            self.assertIn('querySelectorAll(\'[id^="user-content-"]\')', html)

    def test_mixed_case_anchor_handling_in_template(self):
        """Test that template handles mixed case anchor references."""
        markdown_content = '''# Test Document

## Item Section

This is about items.

## CamelCaseSection  

This has mixed case.

## another-section

This is lowercase.
        '''
        
        app = Grip(TextReader(markdown_content, 'test.md'), case_insensitive_anchors=True)
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # The enhanced scrollToHash function should be present
            self.assertIn('anchorId.toLowerCase() === hashTarget.toLowerCase()', html)


    def test_case_insensitive_anchors_enabled(self):
        """Test that case-insensitive anchor handling is included when flag is enabled."""
        from grip import Grip
        from grip.readers import TextReader
        
        markdown_content = '''# Test
        
## Item Section

Some content here.
        '''
        
        # Test with case-insensitive anchors enabled
        app = Grip(TextReader(markdown_content, 'test.md'), case_insensitive_anchors=True)
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Should include case-insensitive anchor logic
            self.assertIn('case-insensitive search', html)
            self.assertIn('hashTarget.toLowerCase()', html)

    def test_case_insensitive_anchors_disabled(self):
        """Test that case-insensitive anchor handling is excluded when flag is disabled."""
        from grip import Grip
        from grip.readers import TextReader
        
        markdown_content = '''# Test
        
## Item Section

Some content here.
        '''
        
        # Test with case-insensitive anchors disabled (default)
        app = Grip(TextReader(markdown_content, 'test.md'), case_insensitive_anchors=False)
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Should NOT include case-insensitive anchor logic
            self.assertNotIn('case-insensitive search', html)
            self.assertNotIn('hashTarget.toLowerCase()', html)
            # Should still have basic scrollToHash function
            self.assertIn('function scrollToHash', html)


if __name__ == '__main__':
    unittest.main()