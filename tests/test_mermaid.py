"""
Tests for Mermaid diagram rendering functionality.
"""

import unittest

from grip.patcher import patch, convert_mermaid_to_div
from grip.renderers import GitHubRenderer


class TestMermaidPatcher(unittest.TestCase):
    """Tests for Mermaid diagram processing in the patcher."""

    def test_mermaid_conversion_disabled_by_default(self):
        """Test that Mermaid conversion is disabled when with_mermaid=False."""
        html_with_mermaid = '''
        <div class="highlight highlight-source-mermaid"><pre><span class="pl-k">classDiagram</span>
<span class="pl-en">Animal</span> <span class="pl-k">&lt;|--</span> <span class="pl-en">Dog</span>
</pre></div>
        '''
        
        result = patch(html_with_mermaid, user_content=False, with_mermaid=False)
        
        # Should preserve original structure when Mermaid is disabled
        self.assertIn('highlight highlight-source-mermaid', result)
        self.assertNotIn('class="mermaid"', result)

    def test_mermaid_conversion_enabled(self):
        """Test that Mermaid conversion works when with_mermaid=True."""
        html_with_mermaid = '''
        <div class="highlight highlight-source-mermaid"><pre><span class="pl-k">classDiagram</span>
<span class="pl-en">Animal</span> <span class="pl-k">&lt;|--</span> <span class="pl-en">Dog</span>
</pre></div>
        '''
        
        result = patch(html_with_mermaid, user_content=False, with_mermaid=True)
        
        # Should convert to Mermaid div when enabled
        self.assertNotIn('highlight highlight-source-mermaid', result)
        self.assertIn('class="mermaid"', result)
        self.assertIn('classDiagram', result)
        self.assertIn('Animal <|-- Dog', result)

    def test_mermaid_multiple_diagrams(self):
        """Test that multiple Mermaid diagrams are all converted."""
        html_with_multiple = '''
        <div class="highlight highlight-source-mermaid"><pre><span class="pl-k">classDiagram</span>
<span class="pl-en">A</span> <span class="pl-k">&lt;|--</span> <span class="pl-en">B</span>
</pre></div>
        <p>Some text</p>
        <div class="highlight highlight-source-mermaid"><pre><span class="pl-k">erDiagram</span>
<span class="pl-en">Customer</span> <span class="pl-sg">{</span>
    <span class="pl-k">string</span> <span class="pl-en">name</span>
<span class="pl-sg">}</span>
</pre></div>
        '''
        
        result = patch(html_with_multiple, user_content=False, with_mermaid=True)
        
        # Should convert both diagrams
        self.assertEqual(result.count('class="mermaid"'), 2)
        self.assertIn('classDiagram', result)
        self.assertIn('erDiagram', result)
        self.assertNotIn('highlight highlight-source-mermaid', result)

    def test_mermaid_with_complex_content(self):
        """Test Mermaid conversion with complex diagram content."""
        html_complex = '''
        <div class="highlight highlight-source-mermaid"><pre><span class="pl-k">classDiagram</span>
<span class="pl-en">Animal</span> <span class="pl-k">&lt;|--</span> <span class="pl-en">Duck</span>
<span class="pl-en">Animal</span> <span class="pl-k">&lt;|--</span> <span class="pl-en">Fish</span>
<span class="pl-en">Animal</span> <span class="pl-k">&lt;|--</span> <span class="pl-en">Zebra</span>
<span class="pl-en">Animal</span> <span class="pl-k">:</span> <span class="pl-k">+int</span> <span class="pl-en">age</span>
<span class="pl-en">Animal</span> <span class="pl-k">:</span> <span class="pl-k">+String</span> <span class="pl-en">gender</span>
<span class="pl-en">Animal</span><span class="pl-k">:</span> <span class="pl-k">+isMammal()</span>
<span class="pl-en">Animal</span><span class="pl-k">:</span> <span class="pl-k">+mate()</span>
</pre></div>
        '''
        
        result = patch(html_complex, user_content=False, with_mermaid=True)
        
        # Should clean up HTML tags and preserve content structure
        self.assertIn('class="mermaid"', result)
        self.assertIn('Animal <|-- Duck', result)
        self.assertIn('+int age', result)
        self.assertIn('+isMammal()', result)
        # Should not contain HTML spans
        self.assertNotIn('<span', result)

    def test_non_mermaid_content_preserved(self):
        """Test that non-Mermaid content is preserved unchanged."""
        html_mixed = '''
        <h1>Title</h1>
        <div class="highlight highlight-source-python"><pre>print("hello")</pre></div>
        <div class="highlight highlight-source-mermaid"><pre><span class="pl-k">classDiagram</span>
<span class="pl-en">A</span> <span class="pl-k">--&gt;</span> <span class="pl-en">B</span>
</pre></div>
        <p>Regular paragraph</p>
        '''
        
        result = patch(html_mixed, user_content=False, with_mermaid=True)
        
        # Should preserve non-Mermaid content
        self.assertIn('<h1>Title</h1>', result)
        self.assertIn('highlight-source-python', result)
        self.assertIn('print("hello")', result)
        self.assertIn('<p>Regular paragraph</p>', result)
        # Should convert Mermaid
        self.assertIn('class="mermaid"', result)
        self.assertNotIn('highlight-source-mermaid', result)


class TestMermaidConverter(unittest.TestCase):
    """Tests for the Mermaid diagram converter function."""

    def test_convert_mermaid_to_div(self):
        """Test the basic Mermaid to div conversion."""
        import re
        
        html_input = '<div class="highlight highlight-source-mermaid"><pre><span class="pl-k">classDiagram</span>\n<span class="pl-en">A</span> <span class="pl-k">&lt;|--</span> <span class="pl-en">B</span>\n</pre></div>'
        
        # Simulate regex match
        pattern = re.compile(r'<div class="highlight highlight-source-mermaid"><pre>(.*?)</pre></div>', re.DOTALL)
        match = pattern.search(html_input)
        
        result = convert_mermaid_to_div(match)
        
        expected = '<div class="mermaid">\nclassDiagram\nA <|-- B\n</div>'
        self.assertEqual(result, expected)

    def test_html_entity_conversion(self):
        """Test that HTML entities are properly converted."""
        import re
        
        html_input = '<div class="highlight highlight-source-mermaid"><pre><span class="pl-en">A</span> <span class="pl-k">&lt;</span> <span class="pl-en">B</span> <span class="pl-k">&gt;</span> <span class="pl-en">C</span>\n</pre></div>'
        
        pattern = re.compile(r'<div class="highlight highlight-source-mermaid"><pre>(.*?)</pre></div>', re.DOTALL)
        match = pattern.search(html_input)
        
        result = convert_mermaid_to_div(match)
        
        # Should convert HTML entities and remove HTML tags
        self.assertIn('A < B > C', result)
        self.assertNotIn('<span', result)


class TestGitHubRendererMermaid(unittest.TestCase):
    """Tests for GitHubRenderer with Mermaid support."""

    def test_renderer_with_mermaid_flag(self):
        """Test that GitHubRenderer accepts the with_mermaid parameter."""
        renderer = GitHubRenderer(with_mermaid=True)
        self.assertTrue(renderer.with_mermaid)
        
        renderer = GitHubRenderer(with_mermaid=False)
        self.assertFalse(renderer.with_mermaid)
        
        # Default should be False
        renderer = GitHubRenderer()
        self.assertFalse(renderer.with_mermaid)

    def test_renderer_parameters_preserved(self):
        """Test that other renderer parameters work with Mermaid flag."""
        renderer = GitHubRenderer(
            user_content=True, 
            context="test/repo",
            api_url="https://api.example.com",
            raw=True,
            with_mermaid=True
        )
        
        self.assertTrue(renderer.user_content)
        self.assertEqual(renderer.context, "test/repo")
        self.assertEqual(renderer.api_url, "https://api.example.com")
        self.assertTrue(renderer.raw)
        self.assertTrue(renderer.with_mermaid)


if __name__ == '__main__':
    unittest.main()